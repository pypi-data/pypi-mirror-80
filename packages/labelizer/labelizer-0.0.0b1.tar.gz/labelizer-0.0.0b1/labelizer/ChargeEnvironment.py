# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:52:03 2017

@author: LAdmin
"""
from Bio.PDB import HSExposure

import numpy as np
#DEBUG
import os
import csv
import logging

from Bio.PDB import NeighborSearch
#from Bio.PDB.NeighborSearch

from .LabelingParameter import LabelingParameter

class ChargeEnvironment(LabelingParameter):
    #constants / parameter
    file_tag = 'ce'
    #class variables
    CHARGE = {'ALA':0,'ARG':1,'ASN':0,'ASP':-1,'CYS':0,'GLU':-1,'GLN':0,'GLY':0,'HIS':1,'ILE':0,
                    'LEU':0,'LYS':1,'MET':0,'PHE':0,'PRO':0,'SER':0,'THR':0,'TRP':0,'TYR':0,'VAL':0}
    protein_charge = 0
    plus_charge = 0
    minus_charge = 0
    
    ### from tryptophan score ###
    RADII = [5, 10, 15, 20]
    WEIGHTS = [100, 40, 20, 10]
    
    HSE_RADIUS = 13.0
    SUM_HSE_THRESH = 30
    SUM_HSE_MAX = 45
    SLOPE_OFFSET=5
    HSE1_THRESH = 10
    HSE1_MAX = 20
    #for charge solvent exposure
    halfSphereExposure = None

    ### NEW ###
    def set_up(self,labelizer,protein,sensitivity='m'):
        super(ChargeEnvironment, self).set_up(labelizer,protein,sensitivity)
        # path1 = os.path.join(labelizer.folder, labelizer.file_extension(protein, 'pdb'))
        # self.load_pdb(path1,protein)
        self.calc_hse()
        self.calc_global_charge()
        atom_list = list(self.structure.get_atoms())
        self.nbSearch = NeighborSearch(atom_list)  
        
    def calc_parameter_score(self,chainId,resIdInt):
        # print("calc_parameter_score")
        residue = self.model[chainId][resIdInt]
        # ca_position = residue['CA'].get_coord()
        ca_position = residue['CA'].get_coord()
        plus_neighbors = []
        minus_neighbors = []
        charge_neighbor_scores = []
        for radius in self.RADII:
            search_result = self.nbSearch.search(ca_position,radius,level='R')
            nbr_plus = 0
            nbr_minus = 0
            count_charge = 0
            for res in search_result:
                try:
                    if self.CHARGE[res.get_resname()]==1 and residue.get_id()!=res.get_id():
                        res2Id = res.get_id()
                        charge_se = self.solvent_exposure(self.halfSphereExposure[chainId+str(res2Id[1])]) #only count tryptophan on surface
                        nbr_plus = nbr_plus + 1
                        count_charge = count_charge + charge_se
                    if self.CHARGE[res.get_resname()]==-1 and residue.get_id()!=res.get_id():
                        res2Id = res.get_id()
                        charge_se = self.solvent_exposure(self.halfSphereExposure[chainId+str(res2Id[1])]) #only count tryptophan on surface
                        nbr_minus = nbr_minus - 1
                        count_charge = count_charge - charge_se
                except:
                    pass
                
            if len(charge_neighbor_scores)>0:
                count_charge=count_charge-sum(charge_neighbor_scores)
                nbr_plus = nbr_plus-sum(plus_neighbors)
                nbr_minus = nbr_minus-sum(minus_neighbors)
            charge_neighbor_scores.append(count_charge)
            plus_neighbors.append(nbr_plus)
            minus_neighbors.append(nbr_minus)
        #TBD fluorophore dependent charge score
        #NOW: completely negative environment: 1, completely positive environment: 0
        charge_score = self.charge_score(plus_neighbors, minus_neighbors)                
        
        return charge_score


   
    # def clean_up(self):
    #     super(ChargeEnvironment, self).clean_up()
    #     # self.save_pdb()
    #     # self.save_csv()
        
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
            
    
    def calc_global_charge(self):
        charge = 0
        pl_charge = 0
        min_charge = 0
        pqr_charge = 0
        pqr_pl_charge = 0
        pqr_min_charge = 0
        path_export = self.file_path[:-4] + "_resCharge.csv"
        # with open(path_export, 'w') as fileW:
        for chain in self.model:
            for residue in chain:
                resId = residue.get_id()
                try:
                    res_name = residue.get_resname()
                    if(res_name=="HOH"):
                        continue
                    sum_atom_charge = 0
                    for atom in residue:
#                        b_fac = atom.get_bfactor()
                        atom_charge = atom.get_occupancy()
                        sum_atom_charge += atom_charge
                        pqr_charge += atom_charge
                        pqr_pl_charge += (atom_charge if atom_charge>0 else 0)
                        pqr_min_charge += (-atom_charge if atom_charge<0 else 0)                          
#                    print resId, res_name
                    # if(res_name=="HOH"):
                    #     print("HOH")
                    res_charge = self.CHARGE[res_name]
                    charge += res_charge
                    pl_charge += (1 if res_charge==1 else 0)
                    min_charge += (1 if res_charge==-1 else 0)
                    # if(abs(sum_atom_charge-res_charge)>0.05):
                    #     print(resId)
                    #     print(np.round(sum_atom_charge,2))
                    #     print(res_charge)
                    line = str(resId[1]) + ',' + res_name + ',' + str(np.round(sum_atom_charge,2)) + '\n'
                    # fileW.write(line) 
                except:
                    # print("FAILED")
                    pass
        self.protein_charge = charge
        self.plus_charge = pl_charge
        self.minus_charge = min_charge
        self.pqr_protein_charge = pqr_charge
        self.pqr_plus_charge = pqr_pl_charge
        self.pqr_minus_charge = pqr_min_charge       

    def charge_score(self, plus_charge, minus_charge):   
        net_charge = np.add(plus_charge, minus_charge)
        # initial_score = np.dot(self.WEIGHTS, net_charge)
        # return initial_score
        sum_charges = np.add(np.abs(plus_charge),np.abs(minus_charge))
        ratio = [(net_ch/sum_ch if sum_ch>0 else 0) for net_ch,sum_ch in zip(net_charge,sum_charges)]
        initial_score = np.dot(self.WEIGHTS, ratio)/sum(self.WEIGHTS)
        
        #SCALING TO 0 - 1
        initial_score = 1-(initial_score+1)/2 #negative charge is prefered
        
        return initial_score
    
    def calc_charges(self):
        return 0


#### TO BE DELETED BELOW ####   

    def calc_charge_score(self):
        logging.warning("deprecated function calc_charge_score")
        filepath = os.path.join(os.path.dirname(self.file_path), self.identifier.lower() +'_chargeAssay.csv')
        # with open(filepath, 'wb') as csv_file:
        with open(filepath, 'w') as csv_file:
            writer = csv.writer(csv_file)
            self.calc_hse()
            atom_list = list(self.structure.get_atoms())
            nbSearch = NeighborSearch(atom_list)
            i=0
            for chain in self.model:
                logging.info("Charge environment {} {}".format(self.identifier, chain.get_id()))
                for residue in chain:
#                for residue in self.model.get_residues():
                    resId = residue.get_id()
#                    if True:
                    try:
                        ca_position = residue['CA'].get_coord()
#                        trp_neighbors = []
#                        trp_neighbor_scores = []
                        plus_neighbors = []
                        minus_neighbors = []
                        charge_neighbor_scores = []
#                        print "Start"
                        for radius in self.RADII:
                            search_result = nbSearch.search(ca_position,radius,level='R')
#                            if residue.get_resname()=='TRP':
#                                count_TRP = 0
#                                nbr_TRP = 0
#                            else:
#                                count_TRP = 0
#                                nbr_TRP = 0
                            nbr_plus = 0
                            nbr_minus = 0
                            count_charge = 0
#                            print search_result
                            for res in search_result:
                                try:
                                    if self.CHARGE[res.get_resname()]==1 and residue.get_id()!=res.get_id():
                                        res2Id = res.get_id()
            #                            print 'get exposure'
                                        charge_se = self.solvent_exposure(self.halfSphereExposure[chain.get_id()+str(res2Id[1])]) #only count tryptophan on surface
                                        nbr_plus = nbr_plus + 1
                                        # if i<1:
                                            # print("+", res2Id, charge_se)
            #                            print 'exposure', trp_se
                                        count_charge = count_charge + charge_se
                                    if self.CHARGE[res.get_resname()]==-1 and residue.get_id()!=res.get_id():
                                        res2Id = res.get_id()
            #                            print 'get exposure'
                                        charge_se = self.solvent_exposure(self.halfSphereExposure[chain.get_id()+str(res2Id[1])]) #only count tryptophan on surface
                                        nbr_minus = nbr_minus - 1
                                        # if i<2:
                                            # print("-", res2Id, charge_se)
                                        count_charge = count_charge - charge_se
                                except:
                                    pass
                            # print(residue.get_id(), count_charge)
                            if len(charge_neighbor_scores)>0:
                                count_charge=count_charge-sum(charge_neighbor_scores)
                                nbr_plus = nbr_plus-sum(plus_neighbors)
                                nbr_minus = nbr_minus-sum(minus_neighbors)
                            charge_neighbor_scores.append(count_charge)
                            plus_neighbors.append(nbr_plus)
                            minus_neighbors.append(nbr_minus)
                        # print(plus_neighbors, minus_neighbors)
                        charge_score = self.charge_score(plus_neighbors, minus_neighbors)
                        #DEBUG
#                        print charge_score
                        writer.writerow([resId, plus_neighbors, minus_neighbors, charge_neighbor_scores, charge_score])
#                        print "written"
            #             if i<5:
            # #                    trp_score = self.tryptophan_score(trp_neighbors)
            #                 print(charge_neighbor_scores, charge_score, plus_neighbors, minus_neighbors)
            #                 i=i+1
                        for atom in residue:
                            atom.set_bfactor(charge_score)
                            parameterKey=chain.get_id()+str(resId[1])
                            self.parameter_score[parameterKey] = charge_score
                    except:
                        # if i<5:
                        #     print("except", residue.get_id())
                        #     i=i+1
                        for atom in residue:
                            atom.set_bfactor(0) 
                        

