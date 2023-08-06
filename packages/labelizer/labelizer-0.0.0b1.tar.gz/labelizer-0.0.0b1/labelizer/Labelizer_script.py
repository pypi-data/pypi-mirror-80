# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:08:30 2017

@author: LAdmin
"""

#Slect Folder: G:\Programming\Labelizer\Development

#%% BLOCK 0
"""
Configuration
"""
protein1 =  '1OMP'      #apo
protein2 = '1ANF'       #holo
proteins = [protein1, protein2]  #,protein2
folder = r'C:\Users\gebha\OneDrive\Dokumente\Python\django-labelizer-test\media'
chainCombination =['A','A']

label_score_model = {'cs':3,'se':3,'tp':0,'cr':0,'ss':0,'ce':0}

#%% BLOCK 0 (a)
"""
Set and alter chain identifier
"""
from AuxiliaryFunction import PDBOperation
import os

for protein in proteins:
    newChain = PDBOperation()
 
    path1 = os.path.join(folder, protein.lower() +'.pdb')
    newChain.load_pdb(path1,protein)
    
    #set chain name or rename chain name
    newChain.set_chain("A")
#    newChain.rename_chain("D","A")
    
    newChain.file_tag = 'A'
    #save modified pdb file
    newChain.save_pdb()   
    
#%% BLOCK 0
"""
Copy conservation score from one chain to the other
"""
from AuxiliaryFunction import ConservationCopy
import os

for protein in proteins:
    #create solvent exposure class and load pdb file
    consCopy = ConservationCopy()

    path1 = os.path.join(folder, protein.lower() +'_With_Conservation_Scores.pdb')
    consCopy.load_pdb(path1,protein)
    
    #calculate half sphere exposure and solvent exposure (can be replaced by other method)
    consCopy.copy_conservation_score(chainCombination[0],chainCombination[1])
    
    #save modified pdb file
    consCopy.save_pdb()
 
#%% BLOCK 1 (a)
"""
Generate all relevant parameters
"""
from SolventExposure import SolventExposure
import os

for protein in proteins:
    #create solvent exposure class and load pdb file
    solEx = SolventExposure()
    #ident = r'1anf'
    #path1 = folder + r'\' + protein1.lower() + '.pdb'
    path1 = os.path.join(folder, protein.lower() + '.pdb')
    solEx.load_pdb(path1,protein)
    
    #calculate half sphere exposure and solvent exposure (can be replaced by other method)
    solEx.calc_hse()
    solEx.set_solvent_exposure()
    
    #save modified pdb file
    solEx.save_pdb()
    solEx.save_csv()

#%% BLOCK 1 (b)

from ConservationScore import ConservationScore
import os

for protein in proteins:
    #create solvent exposure class and load pdb file
    consScore = ConservationScore()
    #ident = r'1anf'
    #path1 = folder + r'\' + protein1.lower() + '.pdb'
    
    #path1 = r'G:\Desktop\Workspace\1anf_cs - Copy.pdb'
    path1 = os.path.join(folder, protein.lower() +'_With_Conservation_Scores.pdb')
    consScore.load_pdb(path1,protein)
    
    #calculate half sphere exposure and solvent exposure (can be replaced by other method)
    consScore.set_conservation_score()
    
    #save modified pdb file
    consScore.save_pdb()
    consScore.save_csv()

#%% BLOCK 1 (c)

from TryptophanProximity import TryptophanProximity
import os

for protein in proteins:
    #create solvent exposure class and load pdb file
    trypProx = TryptophanProximity()
    #ident = r'1anf'
    path1 = os.path.join(folder, protein.lower() + '.pdb')
    #path1 = r'G:\Desktop\Workspace\1anf_cs - Copy.pdb'
    trypProx.load_pdb(path1,protein)
    
    #calculate half sphere exposure and solvent exposure (can be replaced by other method)
    trypProx.calc_tryptophan_score()
    
    #save modified pdb file
    trypProx.save_pdb()
    trypProx.save_csv()

#%% BLOCK 1 (d)

from CysteineResemblance import CysteineResemblance
import os

for protein in proteins:
    #create cysteine resemblance class and load pdb file
    cysRes = CysteineResemblance()
    path1 = os.path.join(folder, protein.lower() + '.pdb')
    cysRes.load_pdb(path1,protein)
    
    #calculate cystein resamblance
    cysRes.calc_resemblance_score()
    
    #save modified pdb file
    cysRes.save_pdb()
    cysRes.save_csv()

#%% BLOCK 1 (e)

from SecondaryStructure import SecondaryStructure
import os

for protein in proteins:
    #create cysteine resemblance class and load pdb file
    secStruc = SecondaryStructure()
    path1 = os.path.join(folder, protein.lower() + '.pdb')
    secStruc.load_pdb(path1,protein)
    
    #calculate cystein resamblance
    secStruc.calc_secondary_structure_score()
    
    #save modified pdb file
    secStruc.save_pdb()
    secStruc.save_csv()

#%% BLOCK 1 (f)

from ChargeEnvironment import ChargeEnvironment
import os

for protein in proteins:
    #create charge environment class and load pdb file
    chargeEnv = ChargeEnvironment()
    path1 = os.path.join(folder, protein.lower() + '.pdb')
    chargeEnv.load_pdb(path1,protein)
    
    #calculate charge environment
    chargeEnv.calc_global_charge()
    print(chargeEnv.protein_charge)
    print(chargeEnv.plus_charge)
    print(chargeEnv.minus_charge)
    chargeEnv.calc_charge_score()
    #save modified pdb file
    chargeEnv.save_pdb()
    chargeEnv.save_csv()

#%% BLOCK 2
"""
Calculate labeling score
"""
import csv
import os

from Bio import PDB
from Bio.PDB import PDBIO

weight_sum = 0
for key, weight in label_score_model.items(): weight_sum += float(weight)
print(weight_sum)
print(label_score_model)
def save_csv(path,dictionary,header):
        with open(path, 'wb') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in dictionary.items():
                line = []
                line.append(key)
                for val in value: line.append(val)
                writer.writerow(line)

for protein in proteins:
    print(protein)               
    label_params = {}
    for key in label_score_model:
        path1 = os.path.join(folder, protein.lower() + r'_' + key + '.csv')
        if label_score_model[key]==0:
            continue
        print(path1)
        with open(path1, 'r') as csv_file:
            reader = csv.reader(csv_file)
            label_params[key] = dict(reader)
    label_score = {}
    label_parameter_score = {}
    for AAkey in label_params[list(label_params.keys())[0]]:
        try:
            score = 0
            parameters = []
            for key in label_score_model:
                #print key
                #print label_score_model[key]
                #print label_params[key][AAkey]
                #print int(label_score_model[key])*int(label_params[key][AAkey])
                if label_score_model[key]==0:
                    pass
                elif float(label_params[key][AAkey])>0:
                    parameters.append(label_params[key][AAkey])
                    score += float(label_score_model[key]/weight_sum)*float(label_params[key][AAkey])
                else:
                    score = 0
                    break
            #print score
        except:
            print(AAkey)
            score = 0
        if score>0:
            parameters.append(score)
            label_parameter_score[AAkey] = parameters
            label_score[AAkey] = [score]
            
    path1 = os.path.join(folder, protein.lower() + '.pdb')
    parser = PDB.PDBParser(PERMISSIVE=1)
    structure = parser.get_structure(protein,path1)
    model=structure[0]
    for chain in model:
            for residue in chain:
                resId = residue.get_id()
                try:
                    parameterKey=chain.get_id()+str(resId[1])                          
                    bFact = label_score[parameterKey][0]
                    for atom in residue:
                        atom.set_bfactor(bFact)
                except:
                    for atom in residue:
                        atom.set_bfactor(0)  

    #save pdb with score
    filepath = os.path.join(folder, protein.lower() + r'_LS.pdb')
    f = open(filepath, 'w')
    io=PDBIO()
    io.set_structure(structure)
    io.save(f)
    
    #save score
    header = str(label_score_model)
    path1 = os.path.join(folder, protein.lower() + r'_LS.csv')
    save_csv(path1,label_score,header)
    path1 = os.path.join(folder, protein.lower() + r'_LSlong.csv')
    save_csv(path1,label_parameter_score,header)
    
#%% BLOCK 3
"""
Calculate PIFE score
"""


#%% BLOCK 4
"""
Calculate FRET score
"""
from FRETScore import FRETScore
import os

fret = FRETScore()
fret.set_foerster_radius(45)

#load calculated labeling scores
apo_path = os.path.join(folder, protein2.lower() + '_LS.csv')
holo_path = os.path.join(folder, protein1.lower() + '_LS.csv')
fret.load_labeling_score(apo_path, protein2,'holo')
fret.load_labeling_score(holo_path, protein1,'apo')
#load pdbs
apo_pdb_path = os.path.join(folder, protein2.lower() + '.pdb')
holo_pdb_path = os.path.join(folder, protein1.lower() + '.pdb')
fret.load_pdb(apo_pdb_path,protein2,'holo')
fret.load_pdb(holo_pdb_path,protein1,'apo')
#calculate pairing score
fret.calc_measurement_scores(chainCombination[0],chainCombination[1])
#export results
fret.save_csv()
fret.save_csv('long')

#%% BLOCK 4 (a)
"""
Calculate FRET score (SINGLE CONFORMATION)
"""
from FRETScore import FRETScore
import os

fret = FRETScore()
fret.set_foerster_radius(50)

#load calculated labeling scores
path = os.path.join(folder, protein1.lower() + '_LS.csv')
fret.load_labeling_score(path, protein1,'apo')
#load pdbs
pdb_path = os.path.join(folder, protein1.lower() + '.pdb')
fret.load_pdb(pdb_path,protein1,'apo')
#calculate pairing score
fret.calc_measurement_scores_single(chainCombination[0],chainCombination[1])
#export results
fret.save_csv()
fret.save_csv('long')
