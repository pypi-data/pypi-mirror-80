# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:52:03 2017

@author: LAdmin
"""
from Bio.PDB import HSExposure

from .LabelingParameter import LabelingParameter
import os
import logging

class SolventExposure(LabelingParameter):
    #constants / parameter
    HSE_RADIUS = 13.0
    file_tag = 'se'
    SUM_HSE_THRESH = 30
    SUM_HSE_MAX = 45
    SLOPE_OFFSET=5
    HSE1_THRESH = 10
    HSE1_MAX = 20
    halfSphereExposure = None

    def set_up(self,labelizer,protein,sensitivity='m'):
        super(SolventExposure, self).set_up(labelizer,protein,sensitivity)
        # path1 = os.path.join(labelizer.folder, labelizer.file_extension(protein, 'pdb'))
        # self.load_pdb(path1,protein)
        self.calc_hse()
        
    def calc_parameter_score(self,chainId,resIdInt):
        hse = self.halfSphereExposure[chainId+str(resIdInt)]
        sumHSE = hse[0]+hse[1]
        sumFact = 1-(sumHSE-self.SUM_HSE_THRESH)*(1./(self.SUM_HSE_MAX-self.SUM_HSE_THRESH+self.SLOPE_OFFSET)) if self.SUM_HSE_THRESH <= sumHSE <= self.SUM_HSE_MAX else (1 if sumHSE<self.SUM_HSE_THRESH else 0)
        hse1Fact = 1-(hse[0]-self.HSE1_THRESH)*(1./self.HSE1_THRESH) if self.HSE1_THRESH <= hse[0] <= self.HSE1_MAX else (1 if hse[0]<self.HSE1_THRESH else 0)

        return sumFact*hse1Fact
    
    # def clean_up(self):
    #     super(SolventExposure, self).clean_up()
    #     # self.save_pdb()
    #     # self.save_csv()
        
    def calc_hse(self):
        hse_cb = HSExposure.HSExposureCB(self.model, self.HSE_RADIUS)
        self.halfSphereExposure = {}
        for key in hse_cb.keys():
            chainId = key[0]
            aminoNbr = key[1][1]
            self.halfSphereExposure[chainId+str(aminoNbr)] = hse_cb[key][0:2]
        

#### TO BE DELETED BELOW ####    
    
    def set_solvent_exposure(self):
        logging.warning("deprecated function set_solvent_exposure")
        for chain in self.model:
            chainId = chain.get_id()
            logging.info("Solvent exposure {} {}".format(self.identifier, chain.get_id()))
            for residue in chain:
                resId = residue.get_id()
                try:                    
                    bFact = self.solvent_exposure(self.halfSphereExposure[chainId+str(resId[1])])
                    for atom in residue:
                        atom.set_bfactor(bFact)
                    parameterKey=chain.get_id()+str(resId[1])
                    self.parameter_score[parameterKey] = bFact
                except:
                    for atom in residue:
                        atom.set_bfactor(0)
        
    
    def solvent_exposure(self,hse):
            sumHSE = hse[0]+hse[1]
            sumFact = 1-(sumHSE-self.SUM_HSE_THRESH)*(1./(self.SUM_HSE_MAX-self.SUM_HSE_THRESH+self.SLOPE_OFFSET)) if self.SUM_HSE_THRESH <= sumHSE <= self.SUM_HSE_MAX else (1 if sumHSE<self.SUM_HSE_THRESH else 0)
            hse1Fact = 1-(hse[0]-self.HSE1_THRESH)*(1./self.HSE1_THRESH) if self.HSE1_THRESH <= hse[0] <= self.HSE1_MAX else (1 if hse[0]<self.HSE1_THRESH else 0)

            return sumFact*hse1Fact
            
