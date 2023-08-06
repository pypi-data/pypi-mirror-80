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

from Bio.PDB import DSSP

# from Bio.PDB import DSSP2
# from Bio.PDB.DSSP2 import DSSP2
# import DSSP2.DSSP as DSSP
# from . import DSSP
# from . import DSSP.DSSP
#from Bio.PDB.NeighborSearch
from .Constants import Constants as CONST
from .LabelingParameter import LabelingParameter

import sys
import warnings
# if not sys.warnoptions:
#     print("SUPPRESS")
#     import warnings
#     warnings.simplefilter("ignore")

class SecondaryStructure(LabelingParameter):
    #constants / parameter
    file_tag = 'ss'
    #class variables
    dssp = None
    #STRUCTURE_VALUE = {'H': alpha-helix, 'B': beta-bridge, 'E': strand (beta-sheet), 'G': 3-10-helix, 'I': pi-helix, 'T': turn, 'S': bend, '-': none}
    STRUCTURE_VALUE = {'H': 0.1, 'B': 0., 'E': 0.2, 'G': 0., 'I': 0., 'T': 1., 'S': 0., '-': 1.}
    MAX_ASA = {'ALA': 106.0, 'ARG': 248.0, 'ASN': 157.0, 'ASP': 163.0, 'CYS': 135.0, 'GLN': 198.0, 'GLU': 194.0, 'GLY': 84.0, 'HIS': 184.0, 'ILE': 169.0,
               'LEU': 164.0, 'LYS': 205.0, 'MET': 188.0, 'PHE': 197.0, 'PRO': 136.0, 'SER': 130.0, 'THR': 142.0, 'TRP': 227.0, 'TYR': 222.0, 'VAL': 142.0}
    structurePosition = None
    #MAX_ASA = dssp.residue_max_acc
    #relative accesible surface area
    #https://en.wikipedia.org/wiki/Relative_accessible_surface_area
    
    # listDSSP = {}

    # def __init__(self):
    #     self.listDSSP = {}
        
    def set_up(self,labelizer,protein,sensitivity='m'):
        super(SecondaryStructure, self).set_up(labelizer,protein,sensitivity)
        # path1 = os.path.join(labelizer.folder, labelizer.file_extension(protein, 'pdb'))
        # self.load_pdb(path1,protein)
        warnings.simplefilter("ignore")

        filepath = os.path.join(os.path.dirname(self.file_path), self.identifier + '.pdb')
        if CONST.PLATFORM=="WINDOWS":
            logging.info("-- windows --")
            self.dssp = DSSP(self.model, filepath, dssp="analysis\dssp\dsspcmbi")
            # print(self.dssp[("A",100)])
            # self.listDSSP = list(self.dssp)
            # print(self.listDSSP)
        elif CONST.PLATFORM=="LINUX":
            logging.info("-- linux --")
            self.dssp = DSSP(self.model, filepath)
            # self.listDSSP = list(self.dssp)
        else:
            raise Exception("Unknown platform")
        # NAME = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLU':'E','GLN':'Q','GLY':'G','HIS':'H','ILE':'I',
        #             'LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
        # filepath = os.path.join(os.path.dirname(self.file_path), self.identifier.lower() +'_ss_test.csv')
        # # with open(filepath, 'wb') as csv_file:
        # with open(filepath, 'w') as file:
        #     # writer = csv.writer(csv_file)
        #     line1 = ''
        #     line2 = ''
        #     line3 = ''
        #     line4 = ''
        #     line5 = ''
        #     line6 = ''
        #     for chain in self.model:
        #         for residue in chain:
        #             resname = residue.get_resname()
        #             resId = residue.get_id()
        #             try:
        #                 name_short = NAME[resname]
        #                 entry = self.dssp[(chain.get_id(),resId[1])]
        #                 line1 += chain.get_id() + ' '*3
        #                 line2 += name_short + ' '*3
        #                 line3 += str(resId[1]) + ' '*(4-len(str(resId[1])))
        #                 line4 += entry[1] + ' '*3
        #                 line5 += str(entry[0]) + ' '*(4-len(str(entry[0])))
        #                 line6 += entry[2] + ' '*3
        #             except:
        #                 continue
        #     line1 += "\n"
        #     line2 += "\n"
        #     line3 += "\n"
        #     file.write(line1)
        #     file.write(line2)
        #     file.write(line3)
        #     line4 += "\n"
        #     line5 += "\n"
        #     line6 += "\n"
        #     file.write(line4)
        #     file.write(line5)
        #     file.write(line6)
        #     # line1 = ""
        #     # line2 = ""
        #     # line3 = ""
        #     # for entry in self.listDSSP:
        #     #     line1 += entry[1] + ' '*3
        #     #     line2 += str(entry[0]) + ' '*(4-len(str(entry[0])))
        #     #     line3 += entry[2] + ' '*3
        #     # line1 += "\n"
        #     # line2 += "\n"
        #     # line3 += "\n"
        #     # file.write(line1)
        #     # file.write(line2)
        #     # file.write(line3)
        
    def calc_parameter_score(self,chainId,resIdInt):
        lastPos = 0
        entry = self.dssp[(chainId,resIdInt)]
        # while(self.listDSSP[lastPos][0]<=resIdInt):
        #     if(self.listDSSP[lastPos][0]==resIdInt):
        #         strTag = self.listDSSP[lastPos][2]
        #     lastPos += 1
        strTag = entry[2]
        structureScore = self.structure_score_simple(strTag)

        return structureScore
    
    # def clean_up(self):
    #     super(SecondaryStructure, self).clean_up()
    #     # self.save_pdb()
    #     # self.save_csv()
        
        
    def structure_score_simple(self,structure_code):   
        return self.STRUCTURE_VALUE[structure_code]
        
#### TO BE DELETED BELOW ####   

    def calc_secondary_structure_score(self):
        logging.warning("deprecated function calc_secondary_structure_score")
        #TODO check case sensitivity -> make everything lower case ?
        warnings.simplefilter("ignore")
        
        filepath = os.path.join(os.path.dirname(self.file_path), self.identifier + '.pdb')
        if CONST.PLATFORM=="WINDOWS":
            logging.info("-- windows --")
            self.dssp = DSSP(self.model, filepath, dssp="analysis\dssp\dsspcmbi")
        elif CONST.PLATFORM=="LINUX":
            logging.info("-- linux --")
            self.dssp = DSSP(self.model, filepath)
        else:
            raise Exception("Unknown platform")
        for chain in self.model:
            # print("Secondary structure ",chain.get_id())
            logging.info("Secondary structure {} {}".format(self.identifier, chain.get_id()))
            # listDSSP = list(self.dssp)
            # print(listDSSP)
            lastPos = 0
            for residue in chain:
                resId = residue.get_id()
#                print(resId)
                try:
#                    res_name = residue.get_resname()
                    resId_nbr = resId[1]
#                    print(resId_nbr)
                    # while(listDSSP[lastPos][0]<=resId_nbr):
                    #     if(listDSSP[lastPos][0]==resId_nbr):
                    #         strTag = listDSSP[lastPos][2]
                    #     lastPos += 1
                    #TBD: CHECK IF PROBLEM WITH NOT CONTINUOUS CHAIN IS SOLVED
                    entry = self.dssp[(chain.get_id(),resId_nbr)]
                    strTag = entry[2]
                    structureScore = self.structure_score_simple(strTag)
#                    print(structureScore)
                    for atom in residue:
                        atom.set_bfactor(structureScore)
                    parameterKey=chain.get_id()+str(resId[1])
                    self.parameter_score[parameterKey] = structureScore
                except:
                    # if CONST.DEBUG:
                    #     print("failed")
                    #     print(resId)
                    for atom in residue:
                        atom.set_bfactor(0)