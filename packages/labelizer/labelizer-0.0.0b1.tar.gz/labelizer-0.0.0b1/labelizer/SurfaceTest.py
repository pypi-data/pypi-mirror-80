# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 18:11:23 2019

@author: LAdmin
"""

#MSMS

from Bio import PDB
from Bio.PDB import PDBIO

from Bio.PDB import ResidueDepth

import os
import csv

protein1 =  '1omp'      #apo
protein2 = '1anf'       #holo
proteins = [protein1, protein2]  #,protein2
folder = r'G:\Desktop\Workspace2'
chainCombination =['A','A']

label_score_model = {'cs':3,'se':3,'tp':0,'cr':1,'ss':1,'ce':1}

#%%

parser = PDB.PDBParser(PERMISSIVE=1)

file_path = os.path.join(folder, protein2.lower() + '.pdb')
identifier = protein2
structure = parser.get_structure(identifier,file_path)
model=structure[0]


#%%
#rd = ResidueDepth(model)
##%%
#surface = ResidueDepth.get_surface("1anf.pdb")
#
#
##%%
#from Bio.PDB.PDBParser import PDBParser
#import Bio.PDB.ResidueDepth as res_depth
#
#parser = PDBParser()
#structure = parser.get_structure('1FAT.pdb')
#model = structure[0]
#
##%%
#from Bio.PDB.PDBParser import PDBParser
#import Bio.PDB.ResidueDepth as res_depth
#
#rd = res_depth(model)
#surface = rd.surface

#%% MSMS
from Bio.PDB.ResidueDepth import get_surface

surface = get_surface(model)


#%%
import numpy as np

i=0
coords = np.array([[0,0,0]])
ids = []
for chain in model:
    for residue in chain:
        if residue.has_id("CA"):
            resId = residue.get_id()[1]
#            print resId
            for atom in residue:
                
#                print atom
#                print atom.coord
                coordLoc=atom.coord
                coords =  np.vstack([coords,atom.coord])
                ids = np.append(ids,resId)
 #np.append([coords], [atom.coord], axis=0) #np.append(coords, atom.coord)
#                print resId, atom
                i += 1


coords = coords[1:,:]

print(coords[0:20])


#%%
i=0
idSurfs = []
#surfaceNp = np.array(surface)
for vertex in surface:
#    print vertex
    ds = vertex - coords
    d2 = np.sqrt(np.sum(ds * ds, 1))
#    print np.argmin(d2)
    argMin = np.argmin(d2)
    i += 1
    if i<10:
        print(argMin, d2[argMin], ids[argMin])
    idSurfs = np.append(idSurfs,ids[argMin])

print(idSurfs[0:20])
#%%
resSurf = np.transpose(np.array([idSurfs,surface[:,0],surface[:,1],surface[:,2]]))

#print resSurf.shape
#print len(resSurf[0])
#print len(resSurf[1])
#print len(resSurf[2])
#print len(resSurf[3])
print(resSurf)

resSurf = resSurf[resSurf[:, 0].argsort()]

print(resSurf[0:20])

#%% Load field
import os


folder = r'G:\Desktop'
filename = 'testarray.npy'
path1 = os.path.join(folder, filename)

potentialMap = np.load(path1)

print(potentialMap[0:5,0:5,0:5])

#%%
center = [5.45, 11.32, 38.88]
dimensions = [161, 129, 161]
size = [83.9620, 71.8180, 80.4490]

def pot_xyz(x, y, z):
#    print x,y,z
#    print center[0]-size[0]/2, center[1]-size[1]/2, center[2]-size[2]/2
    if x<center[0]-size[0]/2 or x>center[0]+size[0]/2 or y<center[1]-size[1]/2 or y>center[1]+size[1]/2 or z<center[2]-size[2]/2 or z>center[2]+size[2]/2:
        raise ValueError('Coordinates out of range.')
    indexX = (x-center[0]+size[0]/2)/size[0]*(dimensions[0]-1)
    indexY = (y-center[1]+size[1]/2)/size[1]*(dimensions[1]-1)
    indexZ = (z-center[2]+size[2]/2)/size[2]*(dimensions[2]-1)
#    print  indexX, indexY, indexZ
    return indexX, indexY, indexZ

#https://en.wikipedia.org/wiki/Trilinear_interpolation
def interpolate(xd,yd,zd,c000,c100,c010,c001,c011,c101,c110,c111):
    a0 = c000
    a1 = -c000 + c100
    a2 = -c000 + c010
    a3 = -c000 + c001
    a4 = c000 - c010 - c100 + c110
    a5 = c000 - c001 - c100 + c101
    a6 = c000 - c010 - c001 + c011
    a7 = -c000 + c001 + c010 + c100 - c011 - c101 - c110 + c111
#    print a0 + a1*xd + a2*yd + a3*zd + a4*xd*yd + a5*xd*zd + a6*yd*zd + a7*xd*yd*zd
    return a0 + a1*xd + a2*yd + a3*zd + a4*xd*yd + a5*xd*zd + a6*yd*zd + a7*xd*yd*zd

def interpolate_pot(x,y,z,arr):
    x,y,z = pot_xyz(x, y, z)
    intX = int(np.floor(x))
    intY = int(np.floor(y))
    intZ = int(np.floor(z))
    xd = x-intX
    yd = y-intY
    zd = z-intZ
#    print xd, yd, zd
    return interpolate(xd,yd,zd,arr[intX,intY,intZ],arr[intX+1,intY,intZ],arr[intX,intY+1,intZ],arr[intX,intY,intZ+1],arr[intX,intY+1,intZ+1],arr[intX+1,intY,intZ+1],arr[intX+1,intY+1,intZ],arr[intX+1,intY+1,intZ+1])

#%% sum residues

potDict = {}
resId = -1
potSum = 0
nbrSurfPoints = 0
for resCoord in resSurf:
    if resId!=resCoord[0]:
#        potLocal = interpolate_pot(resCoord[1],resCoord[2],resCoord[3],potentialMap)
#        potSum += potLocal
#        nbrSurfPoints += 1
#    else:
        if resId!=-1:
#            print resId, potSum, nbrSurfPoints
            potDict[int(resId)] = potSum/nbrSurfPoints
        resId = resCoord[0]
        potSum = 0
        nbrSurfPoints = 0
        
    potLocal = interpolate_pot(resCoord[1],resCoord[2],resCoord[3],potentialMap)
    potSum += potLocal
    nbrSurfPoints += 1
    
#%%
for chain in model:
    
    lastPos = 0
    for residue in chain:
        resId = residue.get_id()
    #    print resId
        try:
            res_name = residue.get_resname()
            resId_nbr = resId[1]
    #        print resId_nbr
    #        print structureScore
            for atom in residue:
                atom.set_bfactor(potDict[resId_nbr])
    #        parameterKey=chain.get_id()+str(resId[1])
    #        self.parameter_score[parameterKey] = structureScore
        except:
            print("failed", resId)
            for atom in residue:
                atom.set_bfactor(0)
                        


#%%

folder = r'G:\Desktop'
file_path = os.path.join(folder, '1anf_pot.pdb')
f = open(file_path, 'w')
io=PDBIO()
io.set_structure(structure)
io.save(f) 
        