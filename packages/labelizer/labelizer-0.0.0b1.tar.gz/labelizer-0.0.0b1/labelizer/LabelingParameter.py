# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 19:02:45 2017

@author: LAdmin
"""
from Bio import PDB
from Bio.PDB import PDBIO

import os
import csv
# import warnings
import logging
logger = logging.getLogger(__name__)

from abc import ABC, abstractmethod
# import .pdbhelper
from . import pdbhelper
# from .pdbhelper import *

class LabelingParameter(ABC):
    #Score for the different parameters that enter in the model of the labeling score
    file_tag = None
    sensitivity = 'm'
    sens_idx = 1
    parameter_score = {}
    identifier = None
    file_path = None
    
    structure = None
    model = None
    chains = None
    
    SENSITIVITY_RANGE =  ['l','m','h']

    def factory(self, t):
        #returns class that has file_tag t (if it cannot find subclass it takes self.__class__)
        klass = next((cls for cls in self.__class__.__subclasses__() if cls.file_tag == t), self.__class__)
        return klass()

    
    ## @abstractmethod
    def set_up(self, labelizer, protein,sensitivity='m'):
        path1 = os.path.join(labelizer.folder, labelizer.file_extension(protein, 'pdb'))
        self.load_pdb(path1,protein)
        pos = labelizer.proteins.index(protein)
        if pos==0:
            self.chains = labelizer.chainCombination
        elif pos==1:
            self.chains = labelizer.chainCombination2
        else:
            NotImplementedError("Maximum 2 protein structures are supported!")
        self.SAVE_PDB = labelizer.SAVE_PDB
        assert sensitivity in self.SENSITIVITY_RANGE, "invalid sensitivity <{}>".format(sensitivity)
        self.sensitivity = sensitivity
        self.sens_idx = self.SENSITIVITY_RANGE.index(self.sensitivity)

    ## @abstractmethod
    def clean_up(self):
        self.save_pdb()
        self.save_csv()
    
    def calc_parameter_scores(self):
        for chain in self.model:
            chainId = chain.get_id()
            if chainId not in self.chains:
                logging.debug("Skip chain {}".format(chainId))
                for residue in chain:
                    for atom in residue:
                        atom.set_bfactor(-1)
            else:
                logging.info("{} {} {}".format(self.__class__,self.identifier, chainId))
                for residue in chain:
                    resId = residue.get_id()
                    parameterKey=chainId+str(resId[1])
                    try:              
                        bFact = self.calc_parameter_score(chainId,resId[1])
                        for atom in residue:
                            atom.set_bfactor(bFact)
                        self.parameter_score[parameterKey] = bFact
                    except Exception as e:
                        #TBD DEBUG ONLY WITH DEBUG FLAG
                        # logger.debug(e)
                        self.parameter_score[parameterKey] = -1
                        for atom in residue:
                            atom.set_bfactor(-1)
        
    # @abstractmethod
    def calc_parameter_score(self,chain,resId):
        pass  


    
    def load_pdb(self,file_path, identifier):
        #warnings.simplefilter("ignore")
        # parser = PDB.PDBParser(PERMISSIVE=1)
        
        self.file_path = file_path
        self.identifier = identifier
        # self.structure = parser.get_structure(identifier,file_path)
        # self.model=self.structure[0]
        
        self.structure,self.model = pdbhelper.load_pdb(identifier,file_path,remove_hetatm=True)
        
        # for chain in self.model:
        #     het_atoms = []
        #     for residue in chain:
        #         res_Id = residue.get_id()
        #         if res_Id[0]!=' ':
        #             #Optional differntiation between water, other HETATM (e.g. ligands, ATP, heavy metal ions)
        #             if res_Id[0]=='W':
        #                 pass
        #             if res_Id[0][:2]=='H_':
        #                 pass
        #             het_atoms.append((res_Id[1],res_Id))
        #     het_atoms.sort(key=lambda x: x[0])
        #     het_atoms.reverse()
        #     for het_id in het_atoms:
        #         chain.detach_child(het_id[1])
                    
        self.parameter_score = {}
        
    # def set_pdb(self,file_path,identifier,structure):
    #     self.file_path = file_path
    #     self.identifier = identifier
    #     self.structure = structure
    #     self.model = self.structure[0]
        
    
    def save_pdb(self):
        if self.SAVE_PDB:
            filepath = os.path.join(os.path.dirname(self.file_path), self.identifier +'_' + self.file_tag + '.pdb')
            # f = open(filepath, 'w')
            pdbhelper.save_pdb(self.structure,filepath)
            # with open(filepath, 'w') as f:
            #     io=PDBIO()
            #     io.set_structure(self.structure)
            #     io.save(f) 
        
    def save_csv(self):
        filepath = os.path.join(os.path.dirname(self.file_path), self.identifier +'_' + self.file_tag + '.csv')
        with open(filepath, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.parameter_score.items():
                writer.writerow([key, value])