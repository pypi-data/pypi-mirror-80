# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 12:29:54 2017

@author: LAdmin
"""
from Bio.PDB import NeighborSearch
from Bio.PDB.vectors import rotaxis

from .MeasurementScore import MeasurementScore
from .Constants import Constants
import numpy as np
from math import pi
import os
import csv
try:
    import LabelLib as ll
    from . import LabelLibFunctions as llf    
    LABELLIB = True
except ImportError:
    LABELLIB = False

import time
import logging

# TBD
# * flag for results (e.g. extendended coord removal, failed, ...)

class FRETScore(MeasurementScore):
    #constants / parameter
    file_tag = 'FRET'
    FOERSTER_RADIUS = 51
    method_options = ["SIMPLE", "GEBHARDT", "KALININ"]
    METHOD = 'SIMPLE' # SIMPLE, GEBHARDT or KALININ
    
    SIMPLE_AV = {}
    SIMPLE_AV_F2 = {}
    AV_CALC_RADIUS = 20.0
    OFFSET_MEAN_AV = 7.5
    SAVE_AV = False
    FOLDER = None
    WEIGHTS = True
    
    COLLISION_RADIUS = 1.7
    
    DEBUG_FRET_SCORE = False
    SAVE_DISTANCE_DATA = True
    
    KALININ_SPEED = ["FAST","PRECISE"][1]
    N_KALININ = {"FAST":10000,"PRECISE":100000}
    GS = {"FAST":1.2,"PRECISE":0.8}
    # dye parameter: linker length, linker width radius 1, radius 2, radius 3
    fluo_parameter = [14.0, 4.5, 5.5, 5.5, 2.0]  #23.5, 4.5, 8.1, 4.2, 1.5
    fluo_parameter2 = [14.0, 4.5, 5.5, 5.5, 2.0]
    #off = 5.2
    LS_THRESHOLD = 0.5
    
    def __init__(self):
        super(FRETScore,self).__init__()
    
    def set_foerster_radius(self,radius):
        self.FOERSTER_RADIUS = radius
    def set_method(self,method):
        if method in self.method_options:
            self.METHOD = method
            # test import DELETE
            if method=="KALININ" and not LABELLIB:
                raise ImportError("AV module LabelLib not installed!")
        else:
            raise ValueError("method must be one of "+str(self.method_options)) 
    def set_offset_AV(self,offset):
        self.OFFSET_MEAN_AV = offset

    def set_save_AV(self, save_AV):
        self.SAVE_AV = save_AV
        
    def set_folder(self, folder):
        self.FOLDER = folder
        
    def set_weights(self,weights):
        self.WEIGHTS = weights
        
    def set_fluorophore(self, fluo1, fluo2):
        self.fluo_parameter = [fluo1['ll'],fluo1['lw'],fluo1['R1'],fluo1['R2'],fluo1['R3']]
        self.fluo_parameter2 = [fluo2['ll'],fluo2['lw'],fluo2['R1'],fluo2['R2'],fluo2['R3']]
        
    def calc_measurement_score(self,ls_apo,ls_apo2,ls_holo,ls_holo2,apo_dist,holo_dist):
        apo_E_acc = self.fret_efficiency(apo_dist)
        holo_E_acc = self.fret_efficiency(holo_dist)
        scoring = self.collective_score(ls_apo,ls_apo2,ls_holo,ls_holo2)
        val = scoring*abs(apo_E_acc-holo_E_acc)
        assert val<=1, "ls_apo {}, ls_apo2 {},ls_holo {}, ls_holo2 {}, apo_dist {}, holo_dist {}, scoring {}, apo_E {}, holo_E {}".format(ls_apo,ls_apo2,ls_holo,ls_holo2,apo_dist,holo_dist,scoring,apo_E_acc,holo_E_acc)
        return val
        
    def collective_score(self,ls_apo,ls_apo2,ls_holo,ls_holo2):
        return 4*ls_apo*ls_apo2*ls_holo*ls_holo2/(ls_apo*ls_apo2*ls_holo+ls_apo*ls_apo2*ls_holo2+ls_apo*ls_holo*ls_holo2+ls_apo2*ls_holo*ls_holo2)
            
    def fret_efficiency(self,r):
        return 1/(1+(r/self.FOERSTER_RADIUS)**6)
        
    def calc_measurement_score_single(self,ls1,ls2,dist):
        E_acc = self.fret_efficiency(dist)
        scoring = self.collective_score_single(ls1,ls2)
        val = scoring*(1-2*abs(E_acc-0.5))
        assert val<=1, "ls1 {}, ls2 {}, dist {}, scoring {}, E {}".format(ls1,ls2,dist,scoring,E_acc)
        return val
    
    def collective_score_single(self,ls1,ls2):
        return 2*ls1*ls2/(ls1+ls2)


    def _get_gly_cb_vector(self, residue):
        """Return a pseudo CB vector for a Gly residue (PRIVATE).
        The pseudoCB vector is centered at the origin.
        CB coord=N coord rotated over -120 degrees
        along the CA-C axis.
        
        Function taken from: Bio/PDB/HSExposure.py
        """
        try:
            n_v = residue["N"].get_vector()
            c_v = residue["C"].get_vector()
            ca_v = residue["CA"].get_vector()
        except Exception:
            return None
        # center at origin
        n_v = n_v - ca_v
        c_v = c_v - ca_v
        # rotation around c-ca over -120 deg
        rot = rotaxis(-pi * 120.0 / 180.0, c_v)
        cb_at_origin_v = n_v.left_multiply(rot)
        ## move back to ca position
        #cb_v = cb_at_origin_v + ca_v
        ## This is for PyMol visualization
        #self.ca_cb_list.append((ca_v, cb_v))
        return cb_at_origin_v

    def calc_simple_AV(self,model,tag,fluo_parameter, chains, fluo_nbr=1):
        atom_list = list(model.get_atoms())
        mean_AV_dict = {}
        nbSearch = NeighborSearch(atom_list)
        logging.debug("Offset mean {}".format(self.OFFSET_MEAN_AV))
        # if fluo_nbr==2:
        #     print("SECOND FLUOROPHORE")
        for chain in model:
            chainId = chain.get_id()
            if chainId not in chains:
                logging.debug("Skip chain {}".format(chainId))
                continue
            logging.info("{} {} {}, fluo {}".format(self.__class__,tag, chainId,fluo_nbr))
            for residue in chain:
                resId = residue.get_id()
                try:
                    if residue.get_resname()!='GLY':
                        cb_position = residue['CB'].get_coord()
                    else:
                        cb_position = self._get_gly_cb_vector(residue)
                        cb_position = residue['CA'].get_coord()+np.array(list(cb_position))
                    search_result = nbSearch.search(cb_position,self.AV_CALC_RADIUS,level='A')
                    coords = []
                    for atom in search_result:
                        coords.append(atom.get_coord())                  
                    mean_atoms = np.mean(coords,axis=0)
                    d = np.linalg.norm(cb_position-mean_atoms)
                    R = self.AV_CALC_RADIUS
                    ll = fluo_parameter[0]
                    if self.OFFSET_MEAN_AV=="auto":
                        b = max(self.COLLISION_RADIUS,2*min(fluo_parameter[2:])-self.COLLISION_RADIUS)
                        off = b + 0.54*ll - 0.0225*ll**2
                    else:
                        off = self.OFFSET_MEAN_AV
                    alpha = np.arccos(1-8/3*d/R)
                    mean_AV = cb_position + (3./4.-d/R)*(fluo_parameter[0]+off)*(cb_position-mean_atoms)/np.linalg.norm(cb_position-mean_atoms)
                    #mean_AV = cb_position + (3./4.-(d-off)/R)*(fluo_parameter[0]+off)*(cb_position-mean_atoms)/np.linalg.norm(cb_position-mean_atoms)

                    parameterKey=chain.get_id()+str(resId[1])
                    mean_AV_dict[parameterKey] = [cb_position, mean_AV,alpha]
                except:
                    if self.DEBUG_FRET_SCORE:
                        logging.debug("Error simple AV, residue {}".format(resId))
                        raise
                    pass
        if fluo_nbr==1:
            self.SIMPLE_AV[tag] = mean_AV_dict
        elif fluo_nbr==2:
            self.SIMPLE_AV_F2[tag] = mean_AV_dict

        if self.SAVE_DISTANCE_DATA:
            try:
                directory = os.path.join(os.path.dirname(self.file_path),self.identifier['apo'] + '_' + self.identifier['holo'] + '_radii_{}_{}_{}'.format(fluo_parameter[2], fluo_parameter[3], fluo_parameter[4]))
            except:
                directory = os.path.join(os.path.dirname(self.file_path),self.identifier['apo'] + '_radii_{}_{}_{}'.format(fluo_parameter[2], fluo_parameter[3], fluo_parameter[4]))
            if not os.path.exists(directory):
                os.makedirs(directory)
            if self.OFFSET_MEAN_AV=='auto':
                filepath = os.path.join(directory, self.identifier[tag] + r'_AV_GEBHARDT_ll{0:.1f}_offAUTO_.csv'.format(fluo_parameter[0]))
            else:
                filepath = os.path.join(directory, self.identifier[tag] + r'_AV_GEBHARDT_ll{0:.1f}_off{1:.1f}_.csv'.format(fluo_parameter[0],off))
            with open(filepath, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)               
                for key, value in self.SIMPLE_AV[tag].items():
                    line = []
                    line.append(key)
                    for val in value: line.append(val)
                    writer.writerow(line)
        return
 
    def generate_coords(self,model):
        coords = []   
        for chain in model:
            for residue in chain: 
                #CHECK RESNAME WATER; IONS; ETC.
                try:
                    res = residue['CA']
                except KeyError as kerr:
                    # print("no CA", residue, residue.get_resname())
                    continue
                if residue.get_resname()=="H20":
                    continue                            
                for atom in residue:
                    vec = atom.get_vector()
                    #ATOMRADIUS TO BE DEFINED
                    coords.append([vec[0],vec[1],vec[2],self.COLLISION_RADIUS])
        logging.debug("Length coords: {}".format(len(coords)))
        return coords

    def save_AVs(self,model,tag,fluo_parameter):
        AV_folder = os.path.join(self.FOLDER,'AVs')
        if not (os.path.exists(AV_folder) and os.path.isdir(AV_folder)):
            os.mkdir(AV_folder)        
        temp_path = os.path.join(self.FOLDER,'AVs',self.identifier[tag] + '_AV' + '_ll_{}_radii_{}_{}_{}'.format(fluo_parameter[0],fluo_parameter[2], fluo_parameter[3], fluo_parameter[4]))
        if not (os.path.exists(temp_path) and os.path.isdir(temp_path)):
            os.mkdir(temp_path)
        
        coords = self.generate_coords(model)
        
        for key, ls in self.labeling_scores['apo'].items():
            try:
                chain = key[0]
                res_nbr = int(key[1:])
                # if res_nbr>100:
                    # raise Exception("Stop")
                res = self.model[tag][chain][res_nbr]
                if res.get_resname()!='GLY':
                    cb_position = np.array(res['CB'].get_coord())
                else:
                    cb_position = self._get_gly_cb_vector(res)
                    cb_position = res['CA'].get_coord()+np.array(list(cb_position))
                cb_position=np.array(cb_position).astype(float)
                
                filename = os.path.join(temp_path, key+'.grid')
                
                #set parameter
                ll = fluo_parameter[0]
                lw = fluo_parameter[1]
                radii = fluo_parameter[2:]
                vdw = self.COLLISION_RADIUS
                gs = self.GS[self.KALININ_SPEED] 
                coords_res = [c for c in coords if not (np.linalg.norm(np.array(c[:3])-cb_position)<lw/2.+vdw+gs)]
                av = llf.calcAV(coords_res, cb_position, linker_length=ll, linker_width=lw, dye_radii=radii,grid_size=gs, save=True, filename=filename)
                filename_xyz = filename[:-4] + "xyz"
                llf.saveXYZ(filename_xyz, av)
            except:
                if self.DEBUG_FRET_SCORE:
                    raise
                logging.debug("Failed to generate AV {}".format(key))
            # if res.get_id()[1]>=29:
            #     raise NotImplementedError("Raise!")
                
    def calc_or_load_AV(self,model,tag,key,fluorophore,load=True,coords=None):
    
        if load: #TBD with fluorophore
            search_path = os.path.join(self.FOLDER,tag+'_AV',key+'.grid')
            if os.path.exists(search_path):
                av = llf.loadAV(search_path)
            else:
                logging.debug("File not found: {}".format(search_path))
                av = None
        else:
            try:
                chain = key[0]
                res_nbr = int(key[1:])
                res = self.model[tag][chain][res_nbr]
                if res.get_resname()!='GLY':
                    cb_position = res['CB'].get_coord()
                else:
                    cb_position = self._get_gly_cb_vector(res)
                    cb_position = res['CA'].get_coord()+np.array(list(cb_position))             
                cb_position=np.array(cb_position).astype(float)

                #set parameter
                ll = fluorophore[0] #self.fluo_parameter[0]
                lw = fluorophore[1] # self.fluo_parameter[1]
                radii = fluorophore[2:] #self.fluo_parameter[2:]
                vdw = self.COLLISION_RADIUS
                gs = self.GS[self.KALININ_SPEED] 
                coords_res = [c for c in coords if not (np.linalg.norm(np.array(c[:3])-cb_position)<lw/2.+vdw+gs)]
                av = llf.calcAV(coords_res, cb_position, linker_length=ll, linker_width=lw, dye_radii=radii,grid_size=gs, save=False)
                if not self.WEIGHTS:
                    av = llf.removeWeights(av)
            except:
                if self.DEBUG_FRET_SCORE:
                    raise
                logging.debug("Failed to generate AV {}".format(key))
                av = None
        return av
    
    # Taken out from 'MeasurementScore.py'            
    def calc_measurement_scores(self,chain1,chain2):
        logging.info("FRET score {} {}".format(chain1, chain2))
        #Test Phase
        distances_apo = {}
        distances_holo = {}
        ## ##
        
#        apo_residues = list(self.model['apo'].get_residues())
        if self.METHOD=="GEBHARDT":
            self.calc_simple_AV(self.model['apo'],'apo', self.fluo_parameter,chain1)
            self.calc_simple_AV(self.model['holo'],'holo',self.fluo_parameter,chain2)
            if self.fluo_parameter!=self.fluo_parameter2:
                self.calc_simple_AV(self.model['apo'],'apo',self.fluo_parameter2,chain1,fluo_nbr=2)
                self.calc_simple_AV(self.model['holo'],'holo',self.fluo_parameter2,chain2,fluo_nbr=2)               
            else:
                self.SIMPLE_AV_F2 = self.SIMPLE_AV
        elif self.METHOD=="KALININ":
            if self.SAVE_AV:
                self.save_AVs(self.model['apo'],'apo',self.fluo_parameter)
                self.save_AVs(self.model['holo'],'holo',self.fluo_parameter)
                if self.fluo_parameter!=self.fluo_parameter2:
                    self.save_AVs(self.model['apo'],'apo',self.fluo_parameter2)
                    self.save_AVs(self.model['holo'],'holo',self.fluo_parameter2)                    
                #pass
                return
            else:
                pass
                # self.save_AVs(self.model['apo'],'apo')
                # self.save_AVs(self.model['holo'],'holo')
            coords_apo = self.generate_coords(self.model['apo'])
            coords_holo = self.generate_coords(self.model['holo'])
#        holo_residues = list(self.model['holo'].get_residues())  
        for apo_key, ls_apo  in self.labeling_scores['apo'].items():
            if self.METHOD=="KALININ":
                logging.debug("KEY ", apo_key)

            if self.LS_THRESHOLD>=float(ls_apo):
                continue
            start = time.time()
            len_pos = 0
            apo_res = self.model['apo'][apo_key[0]][int(apo_key[1:])] 
            try:
                if self.METHOD=="KALININ":                    
                    if self.SAVE_AV and False:
                        apoAV = self.calc_or_load_AV(self.model['apo'],'apo',apo_key,self.fluo_parameter,load=True)
                        holoAV = self.calc_or_load_AV(self.model['holo'],'holo',apo_key,self.fluo_parameter,load=True)
                        if self.fluo_parameter!=self.fluo_parameter2:
                            apoAV_f2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key,self.fluo_parameter2,load=True)
                            holoAV_f2 = self.calc_or_load_AV(self.model['holo'],'holo',apo_key,self.fluo_parameter2,load=True)
                    else:
                        apoAV = self.calc_or_load_AV(self.model['apo'],'apo',apo_key,self.fluo_parameter,load=False,coords=coords_apo)
                        holoAV = self.calc_or_load_AV(self.model['holo'],'holo',apo_key,self.fluo_parameter,load=False,coords=coords_holo)
                        if self.fluo_parameter!=self.fluo_parameter2:
                            apoAV_f2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key,self.fluo_parameter2,load=False,coords=coords_apo)
                            holoAV_f2 = self.calc_or_load_AV(self.model['holo'],'holo',apo_key,self.fluo_parameter2,load=False,coords=coords_holo)                            
                            # if len(apoAV_f2.points()[0])==0 or len(holoAV_f2.points()[0])==0:
                            if len(apoAV_f2.points()[0])<1000 or len(holoAV_f2.points()[0])<1000:
                                logging.debug("{} AV_f2 apo size {}".format(apo_key, len(apoAV_f2.points()[0])))
                                logging.debug("{} AV_f2 holo size {}".format(apo_key, len(holoAV_f2.points()[0])))
                                continue
                        # if len(apoAV.points()[0])==0 or len(holoAV.points()[0])==0:
                        if len(apoAV.points()[0])<1000 or len(holoAV.points()[0])<1000:
                            logging.debug("{} AV apo size {}".format(apo_key, len(apoAV.points()[0])))
                            logging.debug("{} AV holo size {}".format(apo_key, len(holoAV.points()[0])))
                            continue
            except:
                continue
            for apo_key2, ls_apo2  in self.labeling_scores['apo'].items():               
                if apo_key[0]==apo_key2[0] and int(apo_key[1:])>=int(apo_key2[1:]):
                    continue
                if self.LS_THRESHOLD>=float(ls_apo2):
                    continue
                ms_key = str(apo_key) + '_' + str(apo_key2)
                len_pos += 1
                apo_res2 = self.model['apo'][apo_key2[0]][int(apo_key2[1:])]
                if apo_key!=apo_key2 and (chain1[0]==apo_key[0] and chain1[1]==apo_key2[0]):
                    if self.METHOD=="SIMPLE":
                        if apo_res.get_resname()!='GLY':
                            cb_position = apo_res['CB'].get_coord()
                        else:
                            cb_position = self._get_gly_cb_vector(apo_res)
                            cb_position = apo_res['CA'].get_coord()+np.array(list(cb_position)) 
                            
                        if apo_res2.get_resname()!='GLY':
                            cb_position2 = apo_res2['CB'].get_coord()
                        else:
                            cb_position2 = self._get_gly_cb_vector(apo_res2)
                            cb_position2 = apo_res2['CA'].get_coord()+np.array(list(cb_position2))                           
                        
                        apo_distance = np.linalg.norm(np.array(cb_position)-np.array(cb_position2))
                    elif self.METHOD=="GEBHARDT":
                        try:
                            if self.fluo_parameter==self.fluo_parameter2:
                                apoAV = self.SIMPLE_AV['apo'][apo_key]
                                apoAV2 = self.SIMPLE_AV['apo'][apo_key2]
                                apo_distance = np.linalg.norm(np.array(apoAV[1])-np.array(apoAV2[1]))
                                apoAV_f2 = apoAV
                                apoAV2_f2 = apoAV2
                                apo_distance_f2 = apo_distance
                            else:
                                apoAV = self.SIMPLE_AV['apo'][apo_key]
                                apoAV2 = self.SIMPLE_AV['apo'][apo_key2]
                                apoAV_f2 = self.SIMPLE_AV_F2['apo'][apo_key]
                                apoAV2_f2 = self.SIMPLE_AV_F2['apo'][apo_key2]      
                                apo_distance = np.linalg.norm(np.array(apoAV[1])-np.array(apoAV2_f2[1]))
                                apo_distance_f2 = np.linalg.norm(np.array(apoAV_f2[1])-np.array(apoAV2[1]))
                            #Test Phase
                            distances_apo[ms_key] = [apoAV[1][0],apoAV[1][1],apoAV[1][2],apoAV2_f2[1][0],apoAV2_f2[1][1],apoAV2_f2[1][2],apo_distance,apoAV_f2[1][0],apoAV_f2[1][1],apoAV_f2[1][2],apoAV2[1][0],apoAV2[1][1],apoAV2[1][2],apo_distance_f2]
                            ## ##
                        except:
                            if self.DEBUG_FRET_SCORE:
                                raise
                            apo_distance = -1
                    elif self.METHOD=="KALININ":
                        try:
                            if self.SAVE_AV and False:
                                apoAV2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key2,self.fluo_parameter,load=True)
                                if self.fluo_parameter!=self.fluo_parameter2:
                                    apoAV2_f2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key2,self.fluo_parameter2,load=True)
                            else:
                                apoAV2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key2,self.fluo_parameter,load=False,coords=coords_apo)
                                if self.fluo_parameter!=self.fluo_parameter2:
                                    apoAV2_f2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key2,self.fluo_parameter2,load=False,coords=coords_apo)                         

                            # if len(apoAV2.points()[0])==0:
                            if len(apoAV2.points()[0])<1000:
                                logging.debug("{} AV2 apo size {}".format(apo_key2, len(apoAV2.points()[0])))
                                continue
                            # if self.fluo_parameter!=self.fluo_parameter2 and len(apoAV_f2.points()[0])==0:
                            if self.fluo_parameter!=self.fluo_parameter2 and len(apoAV_f2.points()[0])<1000:
                                logging.debug("{} AV2_f2 apo size {}".format(apo_key2, len(apoAV2_f2.points()[0])))
                                continue
                            n = self.N_KALININ[self.KALININ_SPEED]
                            if self.fluo_parameter==self.fluo_parameter2:
                                meanAV = llf.meanAV(apoAV)
                                meanAV2 = llf.meanAV(apoAV2)
                                apo_distance = llf.rmpDistance(apoAV, apoAV2)
                                apo_distanceRDA = llf.rdaDistance(apoAV, apoAV2,n=n)
                                apo_distanceE = llf.effDistance(apoAV, apoAV2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                distances_apo[ms_key] = [meanAV[0],meanAV[1],meanAV[2],meanAV2[0],meanAV2[1],meanAV2[2],apo_distance,apo_distanceRDA,apo_distanceE]
                            else:
                                meanAV = llf.meanAV(apoAV)
                                meanAV2 = llf.meanAV(apoAV2)
                                meanAV_f2 = llf.meanAV(apoAV_f2)
                                meanAV2_f2 = llf.meanAV(apoAV2_f2)
                                apo_distance = llf.rmpDistance(apoAV, apoAV2_f2)
                                apo_distanceRDA = llf.rdaDistance(apoAV, apoAV2_f2,n=n)
                                apo_distanceE = llf.effDistance(apoAV, apoAV2_f2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                apo_distance_f2 = llf.rmpDistance(apoAV_f2, apoAV2)
                                apo_distanceRDA_f2 = llf.rdaDistance(apoAV_f2, apoAV2,n=n)
                                apo_distanceE_f2 = llf.effDistance(apoAV_f2, apoAV2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                distances_apo[ms_key] = [meanAV[0],meanAV[1],meanAV[2],meanAV2_f2[0],meanAV2_f2[1],meanAV2_f2[2],apo_distance,apo_distanceRDA,apo_distanceE,meanAV_f2[0],meanAV_f2[1],meanAV_f2[2],meanAV2[0],meanAV2[1],meanAV2[2],apo_distance_f2,apo_distanceRDA_f2,apo_distanceE_f2]                                
                                # if apo_key=="A29" and apo_key2=="A352":
                                #     #apoAV = llf.removeWeights(apoAV)
                                #     #apoAV2_f2 = llf.removeWeights(apoAV2_f2)
                                #     #ones = np.ones(apoAV.points()[3].shape)
                                #     # apoAV.points = np.array(apoAV.points()[:2],ones)
                                #     #apoAV = ll.addWeights(apoAV,ones)
                                #     #ones = np.ones(apoAV2_f2.points()[3].shape)
                                #     #apoAV2_f2.points = np.array(apoAV2_f2.points()[0],apoAV2_f2.points()[1],apoAV2_f2.points()[2],ones)
                                #     path = r"C:\Users\gebha\OneDrive\Desktop\LabelLib_Test"
                                #     llf.saveXYZ(os.path.join(path,"A29_FS.xyz"),apoAV)
                                #     llf.saveAV(os.path.join(path,"A29_FS.grid"),apoAV)
                                #     llf.saveXYZ(os.path.join(path,"A352_FS.xyz"),apoAV2_f2)
                                #     llf.saveAV(os.path.join(path,"A352_FS.grid"),apoAV2_f2)
                                #     print("R0 ",self.FOERSTER_RADIUS)
                                #     print(llf.rmpDistance(apoAV, apoAV2_f2))
                                #     print(llf.rdaDistance(apoAV, apoAV2_f2,n=100000))
                                #     print(llf.effDistance(apoAV, apoAV2_f2, 67,n=100000))
                                #     testAV1 = llf.loadAV(os.path.join(path,"A29_FS.grid"))
                                #     testAV2 = llf.loadAV(os.path.join(path,"A352_FS.grid"))
                                #     print(llf.rmpDistance(testAV1, testAV2))
                                #     print(llf.rdaDistance(testAV1, testAV2,n=100000))
                                #     print(llf.effDistance(testAV1, testAV2, 67,n=100000))
                                #     print(apoAV.points().T[:10])
                                #     print(testAV1.points().T[:10])
                                #     print("---------------")
                                #     print(apoAV2_f2.points().T[:10])
                                #     print(testAV2.points().T[:10])
                                #     print("---------------")
                                #     av_new = llf.removeWeights(apoAV2_f2)
                                #     print(av_new.points().T[:10])
                                #     # raise NotImplementedError("STOP")
                        except:
                            if self.DEBUG_FRET_SCORE:
                                raise
                            apo_distance = -1
                    else:
                        raise NotImplementedError("Method "+str(self.METHOD)+" not implemented!")

                    try:
                        holo_key = chain2[0] + apo_key[1:]
                        holo_key2 = chain2[1] + apo_key2[1:]
                        
                        holo_res = self.model['holo'][holo_key[0]][int(holo_key[1:])] #holo_residues[apo_key]
                        ls_holo = self.labeling_scores['holo'][holo_key]
                        holo_res2 = self.model['holo'][holo_key2[0]][int(holo_key2[1:])] #holo_residues[apo_key2]
                        ls_holo2 = self.labeling_scores['holo'][holo_key2]
                        if self.METHOD=="SIMPLE":
                            if holo_res.get_resname()!='GLY':
                                cb_position = holo_res['CB'].get_coord()
                            else:
                                cb_position = self._get_gly_cb_vector(holo_res)
                                cb_position = holo_res['CA'].get_coord()+np.array(list(cb_position)) 
                                
                            if holo_res2.get_resname()!='GLY':
                                cb_position2 = holo_res2['CB'].get_coord()
                            else:
                                cb_position2 = self._get_gly_cb_vector(holo_res2)
                                cb_position2 = holo_res2['CA'].get_coord()+np.array(list(cb_position2))                           
                            
                            holo_distance = np.linalg.norm(np.array(cb_position)-np.array(cb_position2))
                            
                        elif self.METHOD=="GEBHARDT":
                            if self.fluo_parameter==self.fluo_parameter2:
                                holoAV = self.SIMPLE_AV['holo'][holo_key]
                                holoAV2 = self.SIMPLE_AV['holo'][holo_key2]
                                holo_distance = np.linalg.norm(np.array(holoAV[1])-np.array(holoAV2[1]))
                                holoAV_f2 = holoAV
                                holoAV2_f2 = holoAV2
                                holo_distance_f2 = holo_distance
                            else:
                                holoAV = self.SIMPLE_AV['holo'][holo_key]
                                holoAV2 = self.SIMPLE_AV['holo'][holo_key2]
                                holoAV_f2 = self.SIMPLE_AV_F2['holo'][holo_key]
                                holoAV2_f2 = self.SIMPLE_AV_F2['holo'][holo_key2]      
                                holo_distance = np.linalg.norm(np.array(holoAV[1])-np.array(holoAV2_f2[1]))
                                holo_distance_f2 = np.linalg.norm(np.array(holoAV_f2[1])-np.array(holoAV2[1]))
                                
                            #Test Phase
                            distances_holo[ms_key] = [holoAV[1][0],holoAV[1][1],holoAV[1][2],holoAV2_f2[1][0],holoAV2_f2[1][1],holoAV2_f2[1][2],holo_distance,holoAV_f2[1][0],holoAV_f2[1][1],holoAV_f2[1][2],holoAV2[1][0],holoAV2[1][1],holoAV2[1][2],holo_distance_f2]
                            
                        elif self.METHOD=="KALININ":
                            if self.SAVE_AV and False:
                                holoAV2 = self.calc_or_load_AV(self.model['holo'],'holo',holo_key2,self.fluo_parameter,load=True)
                                if self.fluo_parameter!=self.fluo_parameter2:
                                    holoAV2_f2 = self.calc_or_load_AV(self.model['holo'],'holo',holo_key2,self.fluo_parameter2,load=True)
                            else:
                                holoAV2 = self.calc_or_load_AV(self.model['holo'],'holo',holo_key2,self.fluo_parameter,load=False,coords=coords_holo)
                                if self.fluo_parameter!=self.fluo_parameter2:
                                    holoAV2_f2 = self.calc_or_load_AV(self.model['holo'],'holo',holo_key2,self.fluo_parameter2,load=False,coords=coords_holo)  
                            # if len(holoAV2.points()[0])==0:
                            if len(holoAV2.points()[0])<1000:
                                logging.debug("{} AV2 holo size {}".format(holo_key2, len(holoAV2.points()[0])))
                                continue
                            # if self.fluo_parameter!=self.fluo_parameter2 and len(holoAV2_f2.points()[0])==0:
                            if self.fluo_parameter!=self.fluo_parameter2 and len(holoAV2_f2.points()[0])<1000:
                                logging.debug("{} AV2_f2 holo size {}".format(holo_key2, len(holoAV2_f2.points()[0])))
                                continue
                            n = self.N_KALININ[self.KALININ_SPEED]
                            if self.fluo_parameter==self.fluo_parameter2:
                                meanAV = llf.meanAV(holoAV)
                                meanAV2 = llf.meanAV(holoAV2)
                                holo_distance = llf.rmpDistance(holoAV, holoAV2)
                                holo_distanceRDA = llf.rdaDistance(holoAV, holoAV2,n=n)
                                holo_distanceE = llf.effDistance(holoAV, holoAV2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                distances_holo[ms_key] = [meanAV[0],meanAV[1],meanAV[2],meanAV2[0],meanAV2[1],meanAV2[2],holo_distance,holo_distanceRDA,holo_distanceE]
                            else:
                                meanAV = llf.meanAV(holoAV)
                                meanAV2 = llf.meanAV(holoAV2)
                                meanAV_f2 = llf.meanAV(holoAV_f2)
                                meanAV2_f2 = llf.meanAV(holoAV2_f2)
                                holo_distance = llf.rmpDistance(holoAV, holoAV2_f2)
                                holo_distanceRDA = llf.rdaDistance(holoAV, holoAV2_f2,n=n)
                                holo_distanceE = llf.effDistance(holoAV, holoAV2_f2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                holo_distance_f2 = llf.rmpDistance(holoAV_f2, holoAV2)
                                holo_distanceRDA_f2 = llf.rdaDistance(holoAV_f2, holoAV2,n=n)
                                holo_distanceE_f2 = llf.effDistance(holoAV_f2, holoAV2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                distances_holo[ms_key] = [meanAV[0],meanAV[1],meanAV[2],meanAV2_f2[0],meanAV2_f2[1],meanAV2_f2[2],holo_distance,holo_distanceRDA,holo_distanceE,meanAV_f2[0],meanAV_f2[1],meanAV_f2[2],meanAV2[0],meanAV2[1],meanAV2[2],holo_distance_f2,holo_distanceRDA_f2,holo_distanceE_f2]  
                        else:
                            raise NotImplementedError("Method "+str(self.METHOD)+" not implemented!")
                        
                        # measurement score
                        ms = self.calc_measurement_score(float(ls_apo),float(ls_apo2),float(ls_holo),float(ls_holo2),apo_distance,holo_distance)
                        self.measurement_score[ms_key] = [ms]
                        self.measurement_score_long[ms_key] = [ls_apo,ls_apo2,ls_holo,ls_holo2,apo_distance,holo_distance,ms]
                    except Exception as ex:
                        if self.DEBUG_FRET_SCORE:
                            raise
                        logging.debug(type(ex).__name__ , holo_key, holo_key2)
                        pass
                # print("GO")
            end = time.time()
            if self.METHOD=="KALININ":
                logging.info("Time for {} steps: {:.1f} s".format(len_pos, end-start))
                logging.info("Estimated remaining time: {:.0f} s".format(len_pos/2*(end-start)))
            
        #Test Phase
        if self.SAVE_DISTANCE_DATA:
            directory = os.path.join(os.path.dirname(self.file_path),self.identifier['apo'] + '_' + self.identifier['holo'] + '_radii1_{}_{}_{}'.format(self.fluo_parameter[2], self.fluo_parameter[3], self.fluo_parameter[4]) + '_radii2_{}_{}_{}'.format(self.fluo_parameter2[2], self.fluo_parameter2[3], self.fluo_parameter2[4]))
            if not os.path.exists(directory):
                os.makedirs(directory)
            if self.METHOD=="GEBHARDT" or self.METHOD=="KALININ":
                if self.METHOD=="GEBHARDT":
                    header = ["KEY","MP1X","MP1Y","MP1Z","MP2X_2","MP2Y_2","MP2Z_2","RMP","MP1X_2","MP1Y_2","MP1Z_2","MP2X","MP2Y","MP2Z","RMP_2"]
                else:
                    header = ["KEY","MP1X","MP1Y","MP1Z","MP2X_2","MP2Y_2","MP2Z_2","RMP","RDA","RDAE","MP1X_2","MP1Y_2","MP1Z_2","MP2X","MP2Y","MP2Z","RMP_2","RDA_2","RDAE_2"]
                if self.METHOD=="GEBHARDT" and self.OFFSET_MEAN_AV!='auto':
                    #filepath_distance_file = os.path.join(os.path.dirname(self.file_path), self.identifier['apo'] +'_AV_' + self.METHOD + '_radius{0:.1f}'.format(self.AV_CALC_RADIUS) + '_off{0:.1f}'.format(self.OFFSET_MEAN_AV) + '.csv')
                    filepath_distance_file = os.path.join(directory, self.identifier['apo'] +'_DIST_' + self.METHOD + '_ll1_{:0.1f}_ll2_{:0.1f}'.format(self.fluo_parameter[0],self.fluo_parameter2[0]) + '_off_{:.1f}'.format(self.OFFSET_MEAN_AV) + '.csv')
                else:
                    filepath_distance_file = os.path.join(directory, self.identifier['apo'] +'_DIST_' + self.METHOD + '_ll1_{:0.1f}_ll2_{:0.1f}'.format(self.fluo_parameter[0],self.fluo_parameter2[0]) + '.csv')
                with open(filepath_distance_file, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file) 
                    writer.writerow(header)
                    for key, value in distances_apo.items():
                        line = []
                        line.append(key)
                        for val in value: line.append(val)
                        writer.writerow(line)
                if self.METHOD=="GEBHARDT" and self.OFFSET_MEAN_AV!='auto':
                    #filepath_distance_file = os.path.join(os.path.dirname(self.file_path), self.identifier['holo'] +'_AV_' + self.METHOD + '_radius{0:.1f}'.format(self.AV_CALC_RADIUS) + '_off{0:.1f}'.format(self.OFFSET_MEAN_AV) + '.csv')
                    filepath_distance_file = os.path.join(directory, self.identifier['holo'] +'_DIST_' + self.METHOD + '_ll1_{:0.1f}_ll2_{:0.1f}'.format(self.fluo_parameter[0],self.fluo_parameter2[0]) + '_off{:.1f}'.format(self.OFFSET_MEAN_AV) + '.csv')
    
                else:
                    filepath_distance_file = os.path.join(directory, self.identifier['holo'] +'_DIST_' + self.METHOD + '_ll1_{:0.1f}_ll2_{:0.1f}'.format(self.fluo_parameter[0],self.fluo_parameter2[0]) + '.csv')
                with open(filepath_distance_file, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file) 
                    writer.writerow(header)
                    for key, value in distances_holo.items():
                        line = []
                        line.append(key)
                        for val in value: line.append(val)
                        writer.writerow(line)
        ## ##
                        
                        
    # TModified from calc_measurement_scores       
    def calc_measurement_scores_single(self,chain1):
        logging.info("FRET score {}".format(chain1))
        #Test Phase
        distances_apo = {}
        ## ##
        
#        apo_residues = list(self.model['apo'].get_residues())
        if self.METHOD=="GEBHARDT":
            self.calc_simple_AV(self.model['apo'],'apo',self.fluo_parameter,chain1)
            # self.calc_simple_AV(self.model['holo'],'holo',self.fluo_parameter)
            if self.fluo_parameter!=self.fluo_parameter2:
                self.calc_simple_AV(self.model['apo'],'apo',self.fluo_parameter2,chain1,fluo_nbr=2)
                # self.calc_simple_AV(self.model['holo'],'holo',self.fluo_parameter2,fluo_nbr=2)               
            else:
                self.SIMPLE_AV_F2 = self.SIMPLE_AV
        elif self.METHOD=="KALININ":
            if self.SAVE_AV:
                self.save_AVs(self.model['apo'],'apo',self.fluo_parameter)
                # self.save_AVs(self.model['holo'],'holo',self.fluo_parameter)
                if self.fluo_parameter!=self.fluo_parameter2:
                    self.save_AVs(self.model['apo'],'apo',self.fluo_parameter2)
                    # self.save_AVs(self.model['holo'],'holo',self.fluo_parameter2)                    
                #pass
                return
            else:
                pass
                # self.save_AVs(self.model['apo'],'apo')
                # self.save_AVs(self.model['holo'],'holo')
            coords_apo = self.generate_coords(self.model['apo'])
            # coords_holo = self.generate_coords(self.model['holo'])
#        holo_residues = list(self.model['holo'].get_residues())  
        for apo_key, ls_apo  in self.labeling_scores['apo'].items():
            if self.METHOD=="KALININ":
                logging.debug("KEY ", apo_key)

            if self.LS_THRESHOLD>=float(ls_apo):
                continue
            start = time.time()
            len_pos = 0
            apo_res = self.model['apo'][apo_key[0]][int(apo_key[1:])] 
            try:
                if self.METHOD=="KALININ":                    
                    if self.SAVE_AV and False:
                        apoAV = self.calc_or_load_AV(self.model['apo'],'apo',apo_key,self.fluo_parameter,load=True)
                        # holoAV = self.calc_or_load_AV(self.model['holo'],'holo',apo_key,self.fluo_parameter,load=True)
                        if self.fluo_parameter!=self.fluo_parameter2:
                            apoAV_f2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key,self.fluo_parameter2,load=True)
                            # holoAV_f2 = self.calc_or_load_AV(self.model['holo'],'holo',apo_key,self.fluo_parameter2,load=True)
                    else:
                        apoAV = self.calc_or_load_AV(self.model['apo'],'apo',apo_key,self.fluo_parameter,load=False,coords=coords_apo)
                        # holoAV = self.calc_or_load_AV(self.model['holo'],'holo',apo_key,self.fluo_parameter,load=False,coords=coords_holo)
                        if self.fluo_parameter!=self.fluo_parameter2:
                            apoAV_f2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key,self.fluo_parameter2,load=False,coords=coords_apo)
                            # holoAV_f2 = self.calc_or_load_AV(self.model['holo'],'holo',apo_key,self.fluo_parameter2,load=False,coords=coords_holo)                            
                            # if len(apoAV_f2.points()[0])==0 or len(holoAV_f2.points()[0])==0:
                            if len(apoAV_f2.points()[0])<1000:
                                logging.debug("{} AV_f2 size {}".format(apo_key, len(apoAV_f2.points()[0])))
                                # logging.debug("{} AV_f2 holo size {}".format(apo_key, len(holoAV_f2.points()[0])))
                                continue
                        # if len(apoAV.points()[0])==0 or len(holoAV.points()[0])==0:
                        if len(apoAV.points()[0])<1000:
                            logging.debug("{} AV size {}".format(apo_key, len(apoAV.points()[0])))
                            # logging.debug("{} AV holo size {}".format(apo_key, len(holoAV.points()[0])))
                            continue
            except:
                if self.DEBUG_FRET_SCORE:
                    raise
            for apo_key2, ls_apo2  in self.labeling_scores['apo'].items():               
                if apo_key[0]==apo_key2[0] and int(apo_key[1:])>=int(apo_key2[1:]):
                    continue
                if self.LS_THRESHOLD>=float(ls_apo2):
                    continue
                ms_key = str(apo_key) + '_' + str(apo_key2)
                len_pos += 1
                apo_res2 = self.model['apo'][apo_key2[0]][int(apo_key2[1:])]
                if apo_key!=apo_key2 and (chain1[0]==apo_key[0] and chain1[1]==apo_key2[0]):
                    if self.METHOD=="SIMPLE":
                        if apo_res.get_resname()!='GLY':
                            cb_position = apo_res['CB'].get_coord()
                        else:
                            cb_position = self._get_gly_cb_vector(apo_res)
                            cb_position = apo_res['CA'].get_coord()+np.array(list(cb_position)) 
                            
                        if apo_res2.get_resname()!='GLY':
                            cb_position2 = apo_res2['CB'].get_coord()
                        else:
                            cb_position2 = self._get_gly_cb_vector(apo_res2)
                            cb_position2 = apo_res2['CA'].get_coord()+np.array(list(cb_position2))                           
                        
                        apo_distance = np.linalg.norm(np.array(cb_position)-np.array(cb_position2))
                    elif self.METHOD=="GEBHARDT":
                        try:
                            if self.fluo_parameter==self.fluo_parameter2:
                                apoAV = self.SIMPLE_AV['apo'][apo_key]
                                apoAV2 = self.SIMPLE_AV['apo'][apo_key2]
                                apo_distance = np.linalg.norm(np.array(apoAV[1])-np.array(apoAV2[1]))
                                apoAV_f2 = apoAV
                                apoAV2_f2 = apoAV2
                                apo_distance_f2 = apo_distance
                            else:
                                apoAV = self.SIMPLE_AV['apo'][apo_key]
                                apoAV2 = self.SIMPLE_AV['apo'][apo_key2]
                                apoAV_f2 = self.SIMPLE_AV_F2['apo'][apo_key]
                                apoAV2_f2 = self.SIMPLE_AV_F2['apo'][apo_key2]      
                                apo_distance = np.linalg.norm(np.array(apoAV[1])-np.array(apoAV2_f2[1]))
                                apo_distance_f2 = np.linalg.norm(np.array(apoAV_f2[1])-np.array(apoAV2[1]))
                            #Test Phase
                            distances_apo[ms_key] = [apoAV[1][0],apoAV[1][1],apoAV[1][2],apoAV2_f2[1][0],apoAV2_f2[1][1],apoAV2_f2[1][2],apo_distance,apoAV_f2[1][0],apoAV_f2[1][1],apoAV_f2[1][2],apoAV2[1][0],apoAV2[1][1],apoAV2[1][2],apo_distance_f2]
                            ## ##
                        except:
                            if self.DEBUG_FRET_SCORE:
                                raise
                            apo_distance = -1
                    elif self.METHOD=="KALININ":
                        try:
                            if self.SAVE_AV and False:
                                apoAV2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key2,self.fluo_parameter,load=True)
                                if self.fluo_parameter!=self.fluo_parameter2:
                                    apoAV2_f2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key2,self.fluo_parameter2,load=True)
                            else:
                                apoAV2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key2,self.fluo_parameter,load=False,coords=coords_apo)
                                if self.fluo_parameter!=self.fluo_parameter2:
                                    apoAV2_f2 = self.calc_or_load_AV(self.model['apo'],'apo',apo_key2,self.fluo_parameter2,load=False,coords=coords_apo)                         

                            # if len(apoAV2.points()[0])==0:
                            if len(apoAV2.points()[0])<1000:
                                logging.debug("{} AV2 size {}".format(apo_key2, len(apoAV2.points()[0])))
                                continue
                            # if self.fluo_parameter!=self.fluo_parameter2 and len(apoAV_f2.points()[0])==0:
                            if self.fluo_parameter!=self.fluo_parameter2 and len(apoAV_f2.points()[0])<1000:
                                logging.debug("{} AV2_f2 size {}".format(apo_key2, len(apoAV2_f2.points()[0])))
                                continue
                            n = self.N_KALININ[self.KALININ_SPEED]
                            if self.fluo_parameter==self.fluo_parameter2:
                                meanAV = llf.meanAV(apoAV)
                                meanAV2 = llf.meanAV(apoAV2)
                                apo_distance = llf.rmpDistance(apoAV, apoAV2)
                                apo_distanceRDA = llf.rdaDistance(apoAV, apoAV2,n=n)
                                apo_distanceE = llf.effDistance(apoAV, apoAV2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                distances_apo[ms_key] = [meanAV[0],meanAV[1],meanAV[2],meanAV2[0],meanAV2[1],meanAV2[2],apo_distance,apo_distanceRDA,apo_distanceE]
                            else:
                                meanAV = llf.meanAV(apoAV)
                                meanAV2 = llf.meanAV(apoAV2)
                                meanAV_f2 = llf.meanAV(apoAV_f2)
                                meanAV2_f2 = llf.meanAV(apoAV2_f2)
                                apo_distance = llf.rmpDistance(apoAV, apoAV2_f2)
                                apo_distanceRDA = llf.rdaDistance(apoAV, apoAV2_f2,n=n)
                                apo_distanceE = llf.effDistance(apoAV, apoAV2_f2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                apo_distance_f2 = llf.rmpDistance(apoAV_f2, apoAV2)
                                apo_distanceRDA_f2 = llf.rdaDistance(apoAV_f2, apoAV2,n=n)
                                apo_distanceE_f2 = llf.effDistance(apoAV_f2, apoAV2, self.FOERSTER_RADIUS,n=n) #, , self.FOERSTER_RADIUS
                                distances_apo[ms_key] = [meanAV[0],meanAV[1],meanAV[2],meanAV2_f2[0],meanAV2_f2[1],meanAV2_f2[2],apo_distance,apo_distanceRDA,apo_distanceE,meanAV_f2[0],meanAV_f2[1],meanAV_f2[2],meanAV2[0],meanAV2[1],meanAV2[2],apo_distance_f2,apo_distanceRDA_f2,apo_distanceE_f2]                                
                                # if apo_key=="A29" and apo_key2=="A352":
                                #     #apoAV = llf.removeWeights(apoAV)
                                #     #apoAV2_f2 = llf.removeWeights(apoAV2_f2)
                                #     #ones = np.ones(apoAV.points()[3].shape)
                                #     # apoAV.points = np.array(apoAV.points()[:2],ones)
                                #     #apoAV = ll.addWeights(apoAV,ones)
                                #     #ones = np.ones(apoAV2_f2.points()[3].shape)
                                #     #apoAV2_f2.points = np.array(apoAV2_f2.points()[0],apoAV2_f2.points()[1],apoAV2_f2.points()[2],ones)
                                #     path = r"C:\Users\gebha\OneDrive\Desktop\LabelLib_Test"
                                #     llf.saveXYZ(os.path.join(path,"A29_FS.xyz"),apoAV)
                                #     llf.saveAV(os.path.join(path,"A29_FS.grid"),apoAV)
                                #     llf.saveXYZ(os.path.join(path,"A352_FS.xyz"),apoAV2_f2)
                                #     llf.saveAV(os.path.join(path,"A352_FS.grid"),apoAV2_f2)
                                #     print("R0 ",self.FOERSTER_RADIUS)
                                #     print(llf.rmpDistance(apoAV, apoAV2_f2))
                                #     print(llf.rdaDistance(apoAV, apoAV2_f2,n=100000))
                                #     print(llf.effDistance(apoAV, apoAV2_f2, 67,n=100000))
                                #     testAV1 = llf.loadAV(os.path.join(path,"A29_FS.grid"))
                                #     testAV2 = llf.loadAV(os.path.join(path,"A352_FS.grid"))
                                #     print(llf.rmpDistance(testAV1, testAV2))
                                #     print(llf.rdaDistance(testAV1, testAV2,n=100000))
                                #     print(llf.effDistance(testAV1, testAV2, 67,n=100000))
                                #     print(apoAV.points().T[:10])
                                #     print(testAV1.points().T[:10])
                                #     print("---------------")
                                #     print(apoAV2_f2.points().T[:10])
                                #     print(testAV2.points().T[:10])
                                #     print("---------------")
                                #     av_new = llf.removeWeights(apoAV2_f2)
                                #     print(av_new.points().T[:10])
                                #     # raise NotImplementedError("STOP")
                        except:
                            if self.DEBUG_FRET_SCORE:
                                raise
                            apo_distance = -1
                    else:
                        raise NotImplementedError("Method "+str(self.METHOD)+" not implemented!")

                    try:           
                        # # measurement score
                        ms = self.calc_measurement_score_single(float(ls_apo),float(ls_apo2),apo_distance)
                        self.measurement_score[ms_key] = [ms]
                        self.measurement_score_long[ms_key] = [ls_apo,ls_apo2,apo_distance,ms]
                    except Exception as ex:
                        if self.DEBUG_FRET_SCORE:
                            raise
                        logging.debug(type(ex).__name__ , apo_key, apo_key2)
                        pass
                # print("GO")
            end = time.time()
            if self.METHOD=="KALININ":
                logging.info("Time for {} steps: {:.1f} s".format(len_pos, end-start))
                logging.info("Estimated remaining time: {:.0f} s".format(len_pos/2*(end-start)))