# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:52:03 2017

@author: LAdmin
"""
import logging
import os
import warnings

from Bio import PDB
from .LabelingParameter import LabelingParameter

class ConservationScore(LabelingParameter):
    #constants / parameter
    file_tag = 'cs'
    #class variables
#    structure = None
#    model = None
    #different scores for sensitivity ['l', 'm', 'h']
    MAX_SCORE = [0.78, 0.84,1.0]    #threshold for conservation score 1 (theoretical lower limit when parameter is 1)
    MIN_SCORE = [-0.04,0.12,0.28]    #threshold for conservation score 4 (theoretical limit when parameter is 0)
    THRESHOLD = [0.2,  0.36,0.52]    #threshold for conservation score 3 (set all parameter values to 0 below threshold, despite zero would be only for values smaller MIN_SCORE)

    cs_files = {}

    def __init__(self):
        self.cs_files = {}

    def set_up(self,labelizer,protein,sensitivity='m'):
        super(ConservationScore, self).set_up(labelizer,protein,sensitivity)
        # path1 = os.path.join(labelizer.folder, labelizer.file_extension(protein, 'pdb'))
        # self.load_pdb(path1,protein)
        protein_position = labelizer.proteins.index(protein)
        #needed because __init__ is only called once
        self.cs_files = {}
        for c,p in zip(labelizer.chainCombination, labelizer.prot_cs[protein_position]):
            
            if c not in self.cs_files:
                #file_path = os.path.join(labelizer.folder, labelizer.file_extension(p,'pdb'))
                file_path = os.path.join(labelizer.folder, p)
                self.load_cs_file(labelizer,file_path,protein,c)
        
    def calc_parameter_score(self,chainId,resIdInt):
        #TO BE CHANGED
        #bFact = next(self.cs_files[chainId][chainId][resIdInt].get_atoms()).get_bfactor()
        bFact = self.cs_files[chainId][chainId+str(resIdInt)]
        conservationScore = self.conservation_score(bFact)
        return conservationScore
    
    # def clean_up(self):
    #     super(ConservationScore, self).clean_up()
    #     # self.save_pdb()
    #     # self.save_csv()



    def load_cs_file(self,labelizer,file_path,identifier,tag):
        cs_dict = {}
        try:
            ext = file_path.split(".")[-1]
        except:
            raise ValueError("unknown file extension: {}".format("None")) 
        if ext=='pdb':
            parser = PDB.PDBParser(PERMISSIVE=1)
            structure = None
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                structure = parser.get_structure(identifier,file_path)
            for chain in structure[0]:
                chainId = chain.get_id()
                if chainId==tag:
                    for residue in chain:
                        try:
                            resId = str(residue.get_id()[1])
                            bFact = next(residue.get_atoms()).get_bfactor()
                            cs_dict[chainId+resId] = bFact
                        except:
                            continue
        elif ext=='grades':
            #pdb_file_path = os.path.join(labelizer.folder,labelizer.file_extension(identifier,'pdb'))
            #structure = parser.get_structure(identifier,pdb_file_path)
            with open(file_path,'r') as grades:
                lines = grades.readlines()
                for line in lines[15:]:
                    try:
                        line_split = line.split('\t')
                        pos = line_split[0].strip()
                        if pos.isdigit():
                            pos = int(pos)
                            #resname = line_split[2].strip()[:3]
                            resId = line_split[2].strip().split(':')[0][3:]
                            chainId = line_split[2].strip().split(':')[1]
                            score = float(line_split[3].strip())
                            #print(resname,resId,chainId,score)
                            cs_dict[chainId+resId] = score
                        else:
                            continue
                    except:
                        continue
            
        else:
            raise ValueError("unknown file extension: {}".format(ext))
        #self.cs_files[tag] = structure[0] 
        self.cs_files[tag] =  cs_dict

    def conservation_score(self,conservation):   
        return 1. if conservation>self.MAX_SCORE[self.sens_idx] else (0. if conservation<self.THRESHOLD[self.sens_idx] else (conservation-self.MIN_SCORE[self.sens_idx])/(self.MAX_SCORE[self.sens_idx]-self.MIN_SCORE[self.sens_idx]))
    
#### TO BE DELETED BELOW ####   
    
    def set_conservation_score(self):
        logging.warning("deprecated function set_conservation_score")
        for chain in self.model:
            logging.info("Conservation score {} {}".format(self.identifier, chain.get_id()))
            for residue in chain:
                resId = residue.get_id()
                try:
                    #print(residue,resId)
                    #REPLACE
                    #bFact = next(residue.get_atoms()).get_bfactor()
                    c_id = chain.get_id()
                    bFact = next(self.cs_files[c_id][c_id][resId[1]].get_atoms()).get_bfactor()
                    
                    conservationScore = self.conservation_score(bFact)
                    #print(conservationScore)
                    for atom in residue:
                        atom.set_bfactor(conservationScore)
                    parameterKey=chain.get_id()+str(resId[1])
                    self.parameter_score[parameterKey] = conservationScore
                except:
                    for atom in residue:
                        atom.set_bfactor(0)                    
    