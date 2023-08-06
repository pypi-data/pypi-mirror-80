# -*- coding: utf-8 -*-

#%% BLOCK 0
"""
Configuration
"""
protein1 =  '1omp'      #apo
protein2 = '1anf'       #holo
proteins = [protein1]  #,protein2
folder = r'G:\Desktop\APBS_Workspace\1omp_pdb2pqr_realisticConditions'
chainCombination =['A','A']

label_score_model = {'cs':3,'se':3,'tp':0,'cr':0,'ss':0,'ce':0}

#%% BLOCK 0 (a)
import os
''' Change pqr-file (to pdb-format)'''
for protein in proteins:
    # Read in the file
    path1 = os.path.join(folder, protein.lower() + '.pqr')
    path2 = os.path.join(folder, protein.lower() + '_mod.pqr')
    with open(path1, 'r') as fileR :
        with open(path2, 'w') as fileW:
            for line in fileR:
                if(line[:4]=="ATOM" or line[:6]=="HETATM"):
                    line = line[:60] + line[62:]
                fileW.write(line) 
#%% BLOCK 1 (f)

from ChargeEnvironment import ChargeEnvironment
import os

for protein in proteins:
    #create charge environment class and load pdb file
    chargeEnv = ChargeEnvironment()
    path1 = os.path.join(folder, protein.lower() + '_mod.pqr')
    chargeEnv.load_pdb(path1,protein)
#%%
for protein in proteins:    
    #calculate charge environment
    chargeEnv.calc_global_charge()
    print chargeEnv.protein_charge
    print chargeEnv.plus_charge
    print chargeEnv.minus_charge

    print chargeEnv.pqr_protein_charge
    print chargeEnv.pqr_plus_charge
    print chargeEnv.pqr_minus_charge
#%%
    chargeEnv.calc_charge_score()
    #save modified pdb file
    chargeEnv.save_pdb()
    chargeEnv.save_csv()