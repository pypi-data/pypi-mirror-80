# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 11:30:45 2019

@author: LAdmin

modified from: https://github.com/Fluorescence-Tools/LabelLib/blob/master/FlexLabel/python/usage.py
"""

# Set path: G:\Programming\LabelLib



import LabelLib as ll
import numpy as np

def savePqr(fileName, grid):
  points = grid.points()
  template = 'ATOM{0: 7}   AV  AV{1: 6}{2:12.1f}{3:8.1f}{4:8.1f}{5:8.2f}{6:7.3f}\n'
  r = grid.discStep * 0.5
  with open(fileName, "w") as out:
    for i, p in enumerate(points.T):
      x, y, z, w = p
      sz = template.format(i + 1, 1, x, y, z, w, r)
      out.write(sz)

def savePqrFromAtoms(fileName, atoms):
  sz = 'ATOM{0: 7}    X   X{1: 6}{2:12.1f}{3:8.1f}{4:8.1f}{5:8.2f}{6:7.3f}\n'
  with open(fileName, "w") as out:
    for i,at in enumerate(atoms.T):
      out.write(sz.format(i, i, at[0], at[1], at[2], 1.0, at[3]))

#%%
from Bio.PDB import PDBParser

pdb_id = "1OMP"

p = PDBParser()
s = p.get_structure(pdb_id, "1OMP.pdb")                    

coords = []   
for chains in s:
    for chain in chains:
        for residue in chain:                             
            for atom in residue:
                #print(atom.get_vector())
                vec = atom.get_vector()
                coords.append([vec[0],vec[1],vec[2],1])

#%%

res = 29
res2 = 352
pos_res = [i for i in s[0]["A"][res]["CB"].get_vector()]
pos_res2 = [i for i in s[0]["A"][res2]["CB"].get_vector()]                  
source=np.array(pos_res).astype(float)
source2=np.array(pos_res2).astype(float)  #5.35

#%%
#coords = []    
#for i in range(-30,30,2):
#    for j in range(-30,30,2):
#        for z in range(-4,0,2):
#            coords.append([i,j,z,1])

atoms = np.array(coords).astype(float).T
#source=np.array([0.0, .0, 0.0]).astype(float)
#source2=np.array([0.0, .0, -4]).astype(float)  #5.35

linker_length = 20.0
linker_width = 2.
dye_radius_1 = 3.5 #4.327285425
simulation_grid_spaceing = 1
av1 = ll.dyeDensityAV1(
  atoms, source, 
  linker_length, 
  linker_width, 
  dye_radius_1, 
  simulation_grid_spaceing
)
av2 = ll.dyeDensityAV1(
  atoms, source2, 
  linker_length, 
  linker_width, 
  dye_radius_1, 
  simulation_grid_spaceing
)
#minLengthGrid = ll.minLinkerLength(
#  atoms, source, 
#  linker_length, 
#  linker_width, 
#  dye_radius_1, 
#  simulation_grid_spaceing
#)

# Grid3D initialization
#g = ll.Grid3D(av1.shape, av1.originXYZ, av1.discStep)

#%% 3 Radii example
radii = np.array([6.5,3.5,1.5]).astype(float)
av1 = ll.dyeDensityAV3(
  atoms, source, 
  linker_length, 
  linker_width, 
  radii, 
  simulation_grid_spaceing
)
av2 = ll.dyeDensityAV3(
  atoms, source2, 
  linker_length, 
  linker_width, 
  radii, 
  simulation_grid_spaceing
)

# def calcAV(coords, cb_position, linker_length=20.0, linker_width=2.0, dye_radii=[8.5,3.5,1.5], save=False, filename=None):
#     atoms = np.array(coords).astype(float).T
#     simulation_grid_spacing = 0.4
#     source = np.array(cb_position).astype(float)
#     radii = np.array(dye_radii).astype(float)
#     av = ll.dyeDensityAV3(
#       atoms, source, 
#       linker_length, 
#       linker_width, 
#       radii, 
#       simulation_grid_spacing
#     )

#%%
print('Saving AVs...')
savePqrFromAtoms(pdb_id + '_atoms.pqr', atoms)
savePqr('AV_'+str(res)+'.pqr', av1)
savePqr('AV_'+str(res2)+'.pqr', av2)
#savePqr('minLinkerLength.pqr', minLengthGrid)

#%%
Emean = ll.meanEfficiency(av1,av2,65.0,100000)
print('Emean = {:.3f}'.format(Emean))
#%%
##Contact volume (re)weigting
#labels=np.full([1,atoms.shape[1]],10.123) # density close to surfaceAtoms will be 10.123 units higher
#surfaceAtoms=np.vstack([atoms,labels])
#surfaceAtoms[3]+=2.34 #contact radius is larger than vdW radius
#acv = ll.addWeights(av1,surfaceAtoms)
##acv2 = ll.addWeights(av2,surfaceAtoms)
##savePqr('ACV.pqr', acv)

#Distance distribution
distances = ll.sampleDistanceDistInv(av1,av2,1000000)
freq, bin_edges = np.histogram(distances,bins=25)
edge_centers=bin_edges[:-1]+(bin_edges[1]-bin_edges[0])/2.0
meanDist=np.sum(freq * edge_centers)/np.sum(freq)
print('Mean distance: {:.2f}'.format(meanDist))
print('\nDist.\tFreq.')
hist=np.column_stack([edge_centers,freq])
for e, f in hist:
    print('{:.2f}\t{:.0f}'.format(e,f))
    
    
#%% Test for LabelLibFunctions
import os
import sys
sys.path.insert(1,r'C:\Users\gebha\OneDrive\Dokumente\GitHub\labelizer-backend\analysis')
import numpy as np
import LabelLibFunctions as llf   


res = 29
pos_res = [i for i in s[0]["A"][res]["CB"].get_vector()]                 
source=np.array(pos_res).astype(float)
print(source)

lw = 4.5
gs = 0.84

coords = []   
for chains in s:
    for chain in chains:
        for residue in chain:
            if residue.get_resname()=='HOH':
                # print("continue ",residue.get_resname())
                continue                         
            for atom in residue:
                
                vec = atom.get_vector()
                if np.linalg.norm(np.array([vec[0],vec[1],vec[2]])-np.array(source))<=lw/2+2.:
                    print("Skip point {}".format(np.array([vec[0],vec[1],vec[2]])))
                else:
                    coords.append([vec[0],vec[1],vec[2],2.])

test_file = "test_AV_29.xyz"
av = llf.calcAV(coords, source, linker_length=23.5, linker_width=lw, dye_radii=[8.1,4.2,1.5],grid_size=gs, save=True, filename=test_file)

print(llf.meanAV(av))