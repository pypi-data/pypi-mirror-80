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
coords = []    
for i in range(-30,30,2):
    for j in range(-30,30,2):
        for z in range(-4,0,2):
            coords.append([i,j,z,1])

atoms = np.array(coords).astype(float).T
source=np.array([0.0, .0, 0.0]).astype(float)
source2=np.array([0.0, .0, -4]).astype(float)  #5.35

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
minLengthGrid = ll.minLinkerLength(
  atoms, source, 
  linker_length, 
  linker_width, 
  dye_radius_1, 
  simulation_grid_spaceing
)

# Grid3D initialization
#g = ll.Grid3D(av1.shape, av1.originXYZ, av1.discStep)
#%%
print('Saving AVs...')
savePqrFromAtoms('atoms.pqr', atoms)
savePqr('AV1.pqr', av1)
savePqr('minLinkerLength.pqr', minLengthGrid)
#%%
savePqr('AV2.pqr', av2)
#%%
Emean = ll.meanEfficiency(av1,av2,52.0,100)
print('Emean = {:.3f}'.format(Emean))
#%%
#Contact volume (re)weigting
labels=np.full([1,atoms.shape[1]],10.123) # density close to surfaceAtoms will be 10.123 units higher
surfaceAtoms=np.vstack([atoms,labels])
surfaceAtoms[3]+=2.34 #contact radius is larger than vdW radius
acv = ll.addWeights(av1,surfaceAtoms)
#acv2 = ll.addWeights(av2,surfaceAtoms)
#savePqr('ACV.pqr', acv)

#Distance distribution
distances = ll.sampleDistanceDistInv(acv,acv,1000000)
freq, bin_edges = np.histogram(distances,bins=25)
edge_centers=bin_edges[:-1]+(bin_edges[1]-bin_edges[0])/2.0
meanDist=np.sum(freq * edge_centers)/np.sum(freq)
print('Mean distance: {:.2f}'.format(meanDist))
print('\nDist.\tFreq.')
hist=np.column_stack([edge_centers,freq])
for e, f in hist:
    print('{:.2f}\t{:.0f}'.format(e,f))