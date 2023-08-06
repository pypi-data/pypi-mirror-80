# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:38:48 2017

@author: LAdmin
"""

visited = {}
for line in open('1anf.pdb'):
    list = line.split()
    id = list[0]
    if id == 'ATOM':
        type = list[2]
        if type == 'CA':
            residue = list[3]
            type_of_chain = list[4]
            atom_count = int(list[5])
            position = list[6:8]
            if atom_count >= 0:
                #if type_of_chain not in visited:
                if atom_count !=  10:
                    visited[type_of_chain] = 1
                    print residue,type_of_chain,atom_count,' '.join(position)
                    
 #%%   
import numpy as np

def dist(x,y):   
    return np.sqrt(np.sum((x-y)**2))

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

vicinity = 5
    
def weight(d):
    return gaussian(d, 0, vicinity)
    
from Bio import PDB
from Bio.PDB import HSExposure

#pdb1 = PDB.PDBList()
#pdb1.retrieve_pdb_file("1CRK") #downloads the .pdb file from the internet
parser = PDB.PDBParser(PERMISSIVE=1)

#structure = parser.get_structure("1CRK",r'C:\Users\Sam\AppData\Local\Enthought\Canopy\User\Lib\site-packages\Bio\cr\pdb1crk.ent')
structure = parser.get_structure("1ANF",r'G:\Programming\Labelizer\Development\1anf.pdb')
model=structure[0]
chain=model["A"]
hse = HSExposure.HSExposureCA(model)
#expca=hse.calc_hs_exposure(model,option='CA3')
#print expca[chain[40]]


RADIUS = 13.0
numberMax=20

#print "HSE based on the approximate CA-CB vectors,"
#print "using three consecutive CA positions:"
#hse_ca = HSExposure.HSExposureCA(model, RADIUS)
#i=1
#for key in hse_ca.keys() :
#    print key, hse_ca[key]
#    i = i + 1
#    if i> numberMax:
#        break

print "HSE based on the real CA-CB vectors:"
hse_cb = HSExposure.HSExposureCB(model, RADIUS)
i=1
halfSphereExposure = {}
for key in hse_cb.keys() :
    aminoNbr = key[1][1]
    halfSphereExposure[aminoNbr] = hse_cb[key][0:2]
    if i < numberMax:
        print key, hse_cb[key]
        i = i + 1
    

#print "HSE based on exposure number:"
#hse_cn = HSExposure.ExposureCN(model, RADIUS)
#i=1
#for key in hse_cb.keys() :
#    print key, hse_cn[key]
#    i = i + 1
#    if i> numberMax:
#        break
    
#%%

#Change BFactor

maxCN = 30
maxHalf = 10

def surface_exposed(hse):
    sumHSE = hse[0]+hse[1]
    sumFact = 1-(sumHSE-30)*0.05 if 30 <= sumHSE <= 45 else (1 if sumHSE<30 else 0)
    hse1Fact = 1-(hse[0]-10)*0.1 if 10 <= hse[0] <= 20 else (1 if hse[0]<10 else 0)
#    if hse[0] <= maxHalf and sumHSE <= maxCN:
#        return 2
#    else:
#        return 0
    return sumFact*hse1Fact


print(structure)
print(dir(structure))
Y1 = np.array([0,0,0]) 
i = 1 
for model in structure:
    for chain in model:
        for residue in chain:
            resId = residue.get_id()
            try: 
                #print halfSphereExposure[resId[1]]
                
                bFact = surface_exposed(halfSphereExposure[resId[1]])
                for atom in residue:
                    atom.set_bfactor(bFact)                                  
                    N = atom.get_name()
                    I = atom.get_id()
                    Y = atom.get_coord()                
                    V = atom.get_vector()
                    O = atom.get_occupancy()
                    B = atom.get_bfactor()
                    
                if i< 20:
                    i = i +1
                    print bFact
            except:
                pass                
                #print("Skip")
                    #atom.set_bfactor(2.0)
                    #print(Y, atom.get_bfactor())
                    #exp_ca = hse.calc_hs_exposure(model, option='CA3')
#%%
from Bio.PDB import PDBIO
f = open(r'G:\Programming\Labelizer\test2.pdb', 'w')
io=PDBIO()
io.set_structure(structure)
io.save(f)                  