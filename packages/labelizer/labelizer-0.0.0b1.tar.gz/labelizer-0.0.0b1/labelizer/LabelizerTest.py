# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:55:16 2019

@author: gebha
"""
#path C:\Users\gebha\OneDrive\Dokumente\GitHub\labelizer-backend
#
#

from analysis.Labelizer import Labelizer

#MalE
directory = r'C:\Users\gebha\OneDrive\Desktop\3L6G_3L6H'
protein1 = '3L6G'
protein2 = '3L6H'
chain1 = ['A','A']
chain2 = ['A','A']
mode = 'f' #FRET
#label_score_model = {'cs':3,'se':3,'tp':0,'cr':1,'ss':0,'ce':0}


label_score_model = {'cs':(3,'m'),'se':(3,'m'),'tp':(0,'m'),'cr':(1,'m'),'ss':(0,'m'),'ce':(0,'m')}


#label_score_model = {'cs':(1,'h'),'se':(1,'m'),'tp':(0,'m'),'cr':(0,'m'),'ss':(0,'m'),'ce':(0,'m')}
fluorophore1 = {'ll':23.5,'lw':4.5,'R1':8.1,'R2':4.2,'R3':1.5}



prot1_cs = [protein1 + '_With_Conservation_Scores.pdb',protein1 + '_With_Conservation_Scores.pdb']
prot2_cs = [protein2 + '_With_Conservation_Scores.pdb',protein2 + '_With_Conservation_Scores.pdb']
#,save_pdb=True NOT WORKING
labelizer = Labelizer(mode,protein1,protein2,chain1,chain2,label_score_dict=label_score_model,prot1_cs=prot1_cs,prot2_cs=prot2_cs ,workdir=directory)
#
# directory = r'C:\Users\gebha\OneDrive\Dokumente\GitHub\labelizer-API\examples\example2_full_request'
# protein1 = '2cg9'
# protein2 = ''
# chain1 = ['A','B']
# chain2 = []
# mode = 'l' #FRET
# # label_score_model = {'cs':0,'se':1,'tp':0,'cr':0,'ss':0}
# label_score_model = {'cs':1,'se':0,'tp':0,'cr':0,'ss':0,'ce':0}
# fluorophore1 = {'ll':23.5,'lw':4.5,'R1':8.1,'R2':4.2,'R3':1.5}

# prot1_cs = ['2CG9_A_consurf.grades','2CG9_B_consurf.grades']
# #prot1_cs = ['2CG9_A_With_Conservation_Scores.pdb','2CG9_B_With_Conservation_Scores.pdb']
# prot2_cs = []


# directory = r'C:\Users\gebha\OneDrive\Desktop\example2_full_request'
# protein1 = '2cg9'
# protein2 = ''
# chain1 = ['A','B']
# chain2 = []
# mode = 's' #FRET
# # label_score_model = {'cs':0,'se':1,'tp':0,'cr':0,'ss':0}
# label_score_model = {'cs':1,'se':1,'tp':0,'cr':0,'ss':0,'ce':0}
# fluorophore1 = {'ll':23.5,'lw':4.5,'R1':8.1,'R2':4.2,'R3':1.5}

# prot1_cs = ['2CG9_A_consurf_del5.grades','2CG9_B_consurf.grades']
# #prot1_cs = ['2CG9_A_With_Conservation_Scores.pdb','2CG9_B_With_Conservation_Scores.pdb']
# prot2_cs = []


# labelizer = Labelizer(mode,protein1,protein2,chain1,chain2,label_score_dict=label_score_model,prot1_cs=prot1_cs,prot2_cs=prot2_cs,workdir=directory,save_pdb=True)

#%%

labelizer.calc_parameter_score()

#%%

labelizer.calc_labeling_score()

#%%
fluorophore1 = {'ll':21,'lw':4.5,'R1':8.1,'R2':3.2,'R3':1.5,'name':'Cy3B'}
#fluorophore1 = {'ll':21.0,'lw':4.5,'R1':8.8,'R2':4.2,'R3':1.5,'name':'Alexa555'}
fluorophore2 = {'ll':21,'lw':4.5,'R1':11.0,'R2':4.7,'R3':1.5,'name':'Atto647N'}

labelizer.set_fluorophore(fluo1=fluorophore1, fluo2=fluorophore2)
labelizer.calc_fret_score(foerster_radius=62,method="GEBHARDT",off="auto",save_AV=False,weights=False)
#%%



for ll in [11.0,14.0,17.0,20.0,23.5,27.0]:
    fluorophore1 = {'ll':ll,'lw':4.5,'R1':10.0,'R2':6.0,'R3':2.0,'name':'TEST'}
    fluorophore2 = {'ll':20.0,'lw':4.5,'R1':11.0,'R2':4.7,'R3':1.5,'name':'Alexa647'}
    
    labelizer.set_fluorophore(fluo1=fluorophore1, fluo2=fluorophore1)
    labelizer.calc_fret_score(foerster_radius=65,method="KALININ",off=0.0,save_AV=False)
    for off in range(8):
        labelizer.calc_fret_score(foerster_radius=65,method="GEBHARDT",off=off,save_AV=False)
    labelizer.calc_fret_score(foerster_radius=65,method="GEBHARDT",off="auto",save_AV=False)
#%%

file_path = labelizer.zip_files()
print(file_path)

# spectrum b, blue_white_red, minimum=0, maximum=1