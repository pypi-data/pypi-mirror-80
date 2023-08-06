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

class CysteineResemblance(LabelingParameter):
    #constants / parameter
    file_tag = 'cr'
    #class variables
    RESEMBLANCES = {'ALA':1.,'ARG':0.5,'ASN':0.5,'ASP':0.5,'CYS':1.,'GLU':0.5,'GLN':0.5,'GLY':0.75,'HIS':0.5,'ILE':0.75,
                    'LEU':0.75,'LYS':0.5,'MET':0.75,'PHE':0.75,'PRO':0.75,'SER':1.,'THR':0.5,'TRP':0.75,'TYR':0.5,'VAL':0.75}
    RESEMBLANCES_SHORT = {'A':0.,'R':0.,'N':0.,'D':0.,'C':1.,'E':0.,'Q':0.,'G':0.,'H':0.,'I':0.,
                          'L':0.,'K':0.,'M':0.,'F':0.,'P':0.,'S':0.,'T':0.,'W':0.,'Y':0.,'V':0.}


    # def set_up(self,labelizer,protein):
    #     super(CysteineResemblance, self).set_up(labelizer,protein)
    #     # path1 = os.path.join(labelizer.folder, labelizer.file_extension(protein, 'pdb'))
    #     # self.load_pdb(path1,protein)

        
    def calc_parameter_score(self,chainId,resIdInt):
        # bFact = next(self.cs_files[chainId][chainId][resIdInt].get_atoms()).get_bfactor()
        res_name = self.model[chainId][resIdInt].get_resname()
        
        resemblanceScore = self.resemblance_score(res_name)
        return resemblanceScore
    
    # def clean_up(self):
    #     super(CysteineResemblance, self).clean_up()
    #     # self.save_pdb()
    #     # self.save_csv()
    

    def resemblance_score(self,residue_name):   
        return self.RESEMBLANCES[residue_name]
 
#### TO BE DELETED BELOW ####   
           
    def calc_resemblance_score(self):
        logging.warning("deprecated function calc_resemblance_score")
        for chain in self.model:
            logging.info("Cysteine resemblance {} {}".format(self.identifier, chain.get_id()))
            for residue in chain:
                resId = residue.get_id()
                try:
                    res_name = residue.get_resname()
                    resemblanceScore = self.resemblance_score(res_name)
                    for atom in residue:
                        atom.set_bfactor(resemblanceScore)
                    parameterKey=chain.get_id()+str(resId[1])
                    self.parameter_score[parameterKey] = resemblanceScore
                except:
                    for atom in residue:
                        atom.set_bfactor(0)
                        