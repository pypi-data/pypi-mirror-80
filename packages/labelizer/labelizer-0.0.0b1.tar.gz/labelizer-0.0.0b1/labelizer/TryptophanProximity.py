# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:52:03 2017

@author: LAdmin
"""
from Bio.PDB import HSExposure
from Bio.PDB import NeighborSearch

import numpy as np
import os
import csv
import logging

from .LabelingParameter import LabelingParameter
from .Constants import Constants

class TryptophanProximity(LabelingParameter):
    #constants / parameter
    file_tag = 'tp'
    #class variables
#    structure = None
#    model = None
    RADII = [5, 10, 20, 30, 40]
    WEIGHTS = [100, 40, 15, 5, 2]
    OFFSET = 5. #20
    SUM = 25. #100
    
    HSE_RADIUS = 13.0
    SUM_HSE_THRESH = 30
    SUM_HSE_MAX = 45
    SLOPE_OFFSET=5
    HSE1_THRESH = 10
    HSE1_MAX = 20
    #for tryptophan solven exposure
    halfSphereExposure = None


    ### NEW ###
    def set_up(self,labelizer,protein,sensitivity='m'):
        super(TryptophanProximity, self).set_up(labelizer,protein,sensitivity)
        # path1 = os.path.join(labelizer.folder, labelizer.file_extension(protein, 'pdb'))
        # self.load_pdb(path1,protein)
        self.calc_hse()
        atom_list = list(self.structure.get_atoms())
        self.nbSearch = NeighborSearch(atom_list)  
        
    def calc_parameter_score(self,chainId,resIdInt):
        # print("calc_parameter_score")
        residue = self.model[chainId][resIdInt]
        # ca_position = residue['CA'].get_coord()
        ca_position = residue['CA'].get_coord()
        trp_neighbors = []
        trp_neighbor_scores = []
        for radius in self.RADII:
            search_result = self.nbSearch.search(ca_position,radius,level='R')
            count_TRP = 0
            nbr_TRP = 0
            # if residue.get_resname()=='TRP':
            #     count_TRP = 0
            #     nbr_TRP = 0
            # else:
            #     count_TRP = 0
            #     nbr_TRP = 0
            for res in search_result:
                if res.get_resname()=='TRP' and residue.get_id()!=res.get_id():
                    chain2Id = res.get_parent().get_id()
                    res2Id = res.get_id()
#                            print 'get exposure'
                    trp_se = self.solvent_exposure(self.halfSphereExposure[chain2Id+str(res2Id[1])]) #only count tryptophan on surface
                    nbr_TRP = nbr_TRP + 1
#                            print 'exposure', trp_se
                    count_TRP = count_TRP + trp_se
            if len(trp_neighbor_scores)>0:
                count_TRP=count_TRP-sum(trp_neighbor_scores)
                nbr_TRP = nbr_TRP-sum(trp_neighbors)
            trp_neighbor_scores.append(count_TRP)
            trp_neighbors.append(nbr_TRP)
        trp_score = self.tryptophan_score(trp_neighbor_scores)
        
        return trp_score
    
    # def clean_up(self):
    #     super(TryptophanProximity, self).clean_up()
    #     # self.save_pdb()
    #     # self.save_csv()
        
    ### ###
    def calc_hse(self):
        hse_cb = HSExposure.HSExposureCB(self.model, self.HSE_RADIUS)
        self.halfSphereExposure = {}
        for key in hse_cb.keys():
            chainId = key[0]
            aminoNbr = key[1][1]
            self.halfSphereExposure[chainId+str(aminoNbr)] = hse_cb[key][0:2] 
    # def calc_hse(self):
    #     hse_cb = HSExposure.HSExposureCB(self.model, self.HSE_RADIUS)
    #     self.halfSphereExposure = {}
    #     for key in hse_cb.keys() :
    #         aminoNbr = key[1][1]
    #         self.halfSphereExposure[aminoNbr] = hse_cb[key][0:2]

    def solvent_exposure(self,hse):
            sumHSE = hse[0]+hse[1]
            sumFact = 1-(sumHSE-self.SUM_HSE_THRESH)*(1./(self.SUM_HSE_MAX-self.SUM_HSE_THRESH+self.SLOPE_OFFSET)) if self.SUM_HSE_THRESH <= sumHSE <= self.SUM_HSE_MAX else (1 if sumHSE<self.SUM_HSE_THRESH else 0)
            hse1Fact = 1-(hse[0]-self.HSE1_THRESH)*(1./self.HSE1_THRESH) if self.HSE1_THRESH <= hse[0] <= self.HSE1_MAX else (1 if hse[0]<self.HSE1_THRESH else 0)

            return sumFact*hse1Fact
    
    def tryptophan_neighbors(self,structure,radius):
        return 0
    
    def tryptophan_score(self,neighbors):   
        initial_score = np.dot(self.WEIGHTS,neighbors)
        return 0. if initial_score>self.SUM else (1.-(initial_score-self.OFFSET)/self.SUM if initial_score>=self.OFFSET else 1) 
       
#### TO BE DELETED BELOW ####   
            
        
    def calc_tryptophan_score(self):
        #DEBUG
        # print("CALC TRYPTOPHAN")
        filepath = os.path.join(os.path.dirname(self.file_path), self.identifier.lower() +'_tryptophanAssay.csv')
        with open(filepath, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            self.calc_hse()
            atom_list = list(self.structure.get_atoms())
            nbSearch = NeighborSearch(atom_list)
            i=0
            for chain in self.model:
                logging.info("Tryptophan proximity {} {}".format(self.identifier, chain.get_id()))
                for residue in chain:
#                for residue in self.model.get_residues():
                    resId = residue.get_id()
                    try: 
                        ca_position = residue['CA'].get_coord()
                        trp_neighbors = []
                        trp_neighbor_scores = []
                        for radius in self.RADII:
                            search_result = nbSearch.search(ca_position,radius,level='R')
                            if residue.get_resname()=='TRP':
                                count_TRP = 0
                                nbr_TRP = 0
                            else:
                                count_TRP = 0
                                nbr_TRP = 0
                            for res in search_result:
                                if res.get_resname()=='TRP' and residue.get_id()!=res.get_id():
                                    res2Id = res.get_id()
                                    chain2Id = res.get_parent().get_id()

                #                            print 'get exposure'
                                    trp_se = self.solvent_exposure(self.halfSphereExposure[chain2Id+str(res2Id[1])]) #only count tryptophan on surface
                                    nbr_TRP = nbr_TRP + 1
        #                            print 'exposure', trp_se
                                    count_TRP = count_TRP + trp_se
                            if len(trp_neighbor_scores)>0:
                                count_TRP=count_TRP-sum(trp_neighbor_scores)
                                nbr_TRP = nbr_TRP-sum(trp_neighbors)
                            trp_neighbor_scores.append(count_TRP)
                            trp_neighbors.append(nbr_TRP)
                        trp_score = self.tryptophan_score(trp_neighbor_scores)
                        #DEBUG
                        writer.writerow([resId, trp_neighbors, trp_neighbor_scores,trp_score])
            #             if i<5:
            # #                    trp_score = self.tryptophan_score(trp_neighbors)
            #                 print(trp_neighbor_scores, trp_score)
            #                 i=i+1
                            
            #            if i<0:s
            #                print residue
            #                ca_position = residue['CA'].get_coord() 
            #                print ca_position
            #                search_result = nbSearch.search(ca_position,20,level='R')
            #                print search_result
            #                print residue.get_resname()
            #                i=i+1
                        # if residue.get_resname()=='TRP':
                            # print("Solvent exposure",residue.get_id(), self.solvent_exposure(self.halfSphereExposure[resId[1]]))
    #                        print "Neighbors", trp_neighbor_scores
            #                ca_position = residue['CA'].get_coord() 
            #                print ca_position
            #                search_result = nbSearch.search(ca_position,15,level='R')
            #                print search_result
            #                cntHIS = 0
            #                for res in search_result:
            #                    if res.get_resname()=='HIS':
            #                        cntHIS = cntHIS + 1
            #                print 'neighbored HIS', cntHIS
                        for atom in residue:
                            atom.set_bfactor(trp_score)
                            parameterKey=chain.get_id()+str(resId[1])
                            self.parameter_score[parameterKey] = trp_score
                    except KeyError:   #KeyError as err
                        for atom in residue:
                            atom.set_bfactor(0)  
                    except:
                        raise 
        if Constants.DEBUG:
            logging.debug("write file - To Be Implemented")
                
                