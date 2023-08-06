# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 15:08:30 2017

@author: LAdmin
"""

#Slect Folder: G:\Programming\Labelizer\Development
#from .AuxiliaryFunction import PDBOperation   #, ConservationCopy
import os
import csv
from zipfile import ZipFile  
import logging   
import warnings

from Bio import PDB
from Bio.PDB import PDBIO

from .LabelingParameter import LabelingParameter    
#TBD following imports are required to find right class (check for better solution, e.g. in init file)
from .SolventExposure import SolventExposure
from .ConservationScore import ConservationScore
from .TryptophanProximity import TryptophanProximity
from .CysteineResemblance import CysteineResemblance
from .SecondaryStructure import SecondaryStructure
from .ChargeEnvironment import ChargeEnvironment
from .FRETScore import FRETScore


class Labelizer:    
    # BLOCK 0
    """
    Configuration
    """
    mode = 'f'
    protein1 =  '1OMP'      #apo
    protein2 = '1ANF'       #holo
    proteins = [protein1, protein2]  #,protein
    chainCombination =['A','A']
    chainCombination2 =['A','A']    
    label_score_model = {'cs':3,'se':3,'tp':0,'cr':0,'ss':0,'ce':0}
    
    fluorophore1 = {'ll':23.5,'lw':4.5,'R1':8.1,'R2':4.2,'R3':1.5}
    fluorophore2 = {'ll':23.5,'lw':4.5,'R1':8.1,'R2':4.2,'R3':1.5}
    
    folder = os.path.join('..','media','test')    
    cons_serv_add = '_With_Conservation_Scores.pdb'
    prot1_cs = ''
    prot2_cs = ''
    prot_cs = [prot1_cs,prot2_cs]
    
    LONG_OUTPUT = False
    SAVE_PDB = False
    
    def __init__(self, mode, protein1,protein2,chain1,chain2,label_score_dict,workdir=os.getcwd(),cons_serv_add='_With_Conservation_Scores.pdb',prot1_cs=None,prot2_cs=None,long_output=False,save_pdb=False):
        self.mode = mode
        self.protein1 = self.file_extension(protein1,'pdb')[:-4]  #protein1
        if protein2 is not None:
            self.protein2 = self.file_extension(protein2,'pdb')[:-4]  #protein2
        else:
            self.protein2 = None
        if mode=='f':
            self.proteins = [self.protein1,self.protein2]
        elif mode=='s' or mode=='l':
            self.proteins = [self.protein1]
        else:
            raise NotImplementedError('So far, only fret (f), single FRET (s), and single label (l) modes are available')
        if prot1_cs == None:
            self.prot1_cs = [ self.protein1 + self.file_extension(cons_serv_add,'pdb') for chains in chain1 ]
        else:
            self.prot1_cs = prot1_cs
        if mode=='f':
            if prot2_cs == None:
                self.prot2_cs = [ self.protein2 + self.file_extension(cons_serv_add,'pdb') for chains in chain2  ]
            else:
                self.prot2_cs = prot2_cs
            self.prot_cs = [self.prot1_cs,self.prot2_cs]
        else:
            self.prot_cs = [self.prot1_cs]
        self.chainCombination = [c.upper() for c in chain1] #[chain1,chain2]
        if mode=='f':
            self.chainCombination2 = [c.upper() for c in chain2] #[chain1,chain2]
            
        #TBD sanity check (if model is of right form)
        self.label_score_model = {}
        for key,val in label_score_dict.items():
            if isinstance(val,tuple) or isinstance(val,list) :
                self.label_score_model[key] = tuple(val)
            elif isinstance(val, float) or isinstance(val, int):
                self.label_score_model[key] = (val,'m')
            else:
                raise NotImplementedError("only tuple (weight, sensitivity) or weight is allowed")
                
        
        self.folder = workdir
        
        self.LONG_OUTPUT = long_output
        self.SAVE_PDB = save_pdb
        
    """
    Set fluorophores for analysis
    """    
    def set_fluorophore(self, fluo1=None, fluo2=None):
        self.fluorophore1 = fluo1
        self.fluorophore2 = fluo2
    
#TBD MOVE TO PDBOperation
        
#     """
#     Set and alter chain identifier
#     """
# #    from AuxiliaryFunction import PDBOperation
# #    import os
#     def set_chain(self, prot_nbr, chain_letter):
# #    for protein in proteins:
#         newChain = PDBOperation()
     
#         path1 = os.path.join(self.folder, self.proteins[prot_nbr] +'.pdb')
#         newChain.load_pdb(path1,self.proteins[prot_nbr])
        
#         #set chain name or rename chain name
#         newChain.set_chain(chain_letter)
#     #    newChain.rename_chain("D","A")
        
#         newChain.file_tag = chain_letter
#         #save modified pdb file
#         newChain.save_pdb()   

#     def rename_chain(self, prot_nbr, chain_letter_old, chain_letter_new):
# #    for protein in proteins:
#         newChain = PDBOperation()
     
#         path1 = os.path.join(self.folder, self.proteins[prot_nbr] +'.pdb')
#         newChain.load_pdb(path1,self.proteins[prot_nbr])
        
#         #set chain name or rename chain name
# #        newChain.set_chain(chain_letter)
#         newChain.rename_chain(chain_letter_old,chain_letter_new)
        
#         newChain.file_tag = chain_letter_new
#         #save modified pdb file
#         newChain.save_pdb()   

    def file_extension(self,filename,ext):
        if ext[0]!='.':
            ext = '.' + ext
        assert ('.' not in ext[1:]), "invalid file extension"
        if len(filename)>=len(ext) and filename[-len(ext):]==ext:
            return filename
        else:
            return filename + ext
#    def set_chain(protein, chain_letter):
        
    # BLOCK 0
    """
    Copy conservation score from one chain to the other
    """
# USAGE TO BE CHANGED
#    from AuxiliaryFunction import ConservationCopy

#     def copy_conservation_score(self, prot_nbr):
# #    for protein in proteins:
#         #create solvent exposure class and load pdb file
#         consCopy = ConservationCopy()
    
#         path1 = os.path.join(self.folder, self.proteins[prot_nbr] +'_With_Conservation_Scores.pdb')
#         consCopy.load_pdb(path1,self.proteins[prot_nbr])
        
#         #calculate half sphere exposure and solvent exposure (can be replaced by other method)
#         consCopy.copy_conservation_score(self.chainCombination[0],self.chainCombination[1])
        
#         #save modified pdb file
#         consCopy.save_pdb()

    # BLOCK 1 
    """
    Generate all relevant parameters
    """
    # def calc_parameter_score_old(self):
    #     logging.warning("deprecated calc_parameter_score")
    #     if 'se' in self.label_score_model:
    #         if self.label_score_model['se']>0:
    #             self.calc_solvent_exposure()
    #     if 'cs' in self.label_score_model:
    #         if self.label_score_model['cs']>0:         
    #             self.calc_conservation_score()
    #     if 'tp' in self.label_score_model:
    #         if self.label_score_model['tp']>0:          
    #             self.calc_tryptophan_proximity()
    #     if 'cr' in self.label_score_model:
    #         if self.label_score_model['cr']>0:          
    #             self.calc_cysteine_resemblance()
    #     if 'ss' in self.label_score_model:
    #         if self.label_score_model['ss']>0:        
    #             self.calc_secondary_structure()
    #     if 'ce' in self.label_score_model:
    #         if self.label_score_model['ce']>0:         
    #             self.calc_charge_environment()            

    def calc_parameter_score(self):
        for tag in self.label_score_model.keys():
            if self.label_score_model[tag][0]>0:
                for protein in self.proteins:
                    labelingParamter = LabelingParameter().factory(tag)
                    labelingParamter.set_up(self,protein,self.label_score_model[tag][1])
                    labelingParamter.calc_parameter_scores()
                    labelingParamter.clean_up()
            
#     #### BLOCK 1 TO BE DELETED ####
#     # BLOCK 1 (a)
#     """
#     Generate all relevant parameters
#     """
# #    from SolventExposure import SolventExposure
# #    import os
#     def calc_solvent_exposure(self):
#         for protein in self.proteins:
#             #create solvent exposure class and load pdb file
#             solEx = SolventExposure()
#             path1 = os.path.join(self.folder, protein + '.pdb')
#             solEx.load_pdb(path1,protein)
            
#             #calculate half sphere exposure and solvent exposure (can be replaced by other method)
#             solEx.calc_hse() #<- set_up()
#             solEx.set_solvent_exposure() #<-calc_parameter_score()
            
#             #save modified pdb file
#             solEx.save_pdb()
#             solEx.save_csv()
    
#     # BLOCK 1 (b)
    
# #    from ConservationScore import ConservationScore
# #    import os
#     def calc_conservation_score(self):
#         for idx, protein in enumerate(self.proteins):
#             #create solvent exposure class and load pdb file
#             consScore = ConservationScore()
#             path1 = os.path.join(self.folder, self.file_extension(protein,'pdb'))
#             consScore.load_pdb(path1,protein)
            
#             for c,p in zip(self.chainCombination, self.prot_cs[idx]):
#                 if c not in consScore.cs_files:
#                     file_path = os.path.join(self.folder, self.file_extension(p,'pdb'))
#                     consScore.load_cs_file(file_path,protein,c)
#             #calculate conservation score (can be replaced by other method)
                    
#             consScore.set_conservation_score()
            
#             #save modified pdb file
#             consScore.save_pdb()
#             consScore.save_csv()
    
#     # BLOCK 1 (c)
    
# #    from TryptophanProximity import TryptophanProximity
# #    import os
#     def calc_tryptophan_proximity(self):    
#         for protein in self.proteins:
#             #create solvent exposure class and load pdb file
#             trypProx = TryptophanProximity()
#             path1 = os.path.join(self.folder, self.file_extension(protein,'pdb'))
#             trypProx.load_pdb(path1,protein)
            
#             #calculate half sphere exposure and solvent exposure (can be replaced by other method)
#             trypProx.calc_tryptophan_score()
            
#             #save modified pdb file
#             trypProx.save_pdb()
#             trypProx.save_csv()
    
#     # BLOCK 1 (d)
    
# #    from CysteineResemblance import CysteineResemblance
# #    import os
#     def calc_cysteine_resemblance(self):     
#         for protein in self.proteins:
#             #create cysteine resemblance class and load pdb file
#             cysRes = CysteineResemblance()
#             path1 = os.path.join(self.folder, self.file_extension(protein,'pdb'))
#             cysRes.load_pdb(path1,protein)
            
#             #calculate cystein resamblance
#             cysRes.calc_resemblance_score()
            
#             #save modified pdb file
#             cysRes.save_pdb()
#             cysRes.save_csv()
    
#     # BLOCK 1 (e)
    
# #    from SecondaryStructure import SecondaryStructure
# #    import os
#     def calc_secondary_structure(self):       
#         for protein in self.proteins:
#             #create cysteine resemblance class and load pdb file
#             secStruc = SecondaryStructure()
#             path1 = os.path.join(self.folder, self.file_extension(protein,'pdb'))
#             secStruc.load_pdb(path1,protein)
            
#             #calculate cystein resamblance
#             secStruc.calc_secondary_structure_score()
            
#             #save modified pdb file
#             secStruc.save_pdb()
#             secStruc.save_csv()
    
#     # BLOCK 1 (f)
    
# #    from ChargeEnvironment import ChargeEnvironment
# #    import os
#     def calc_charge_environment(self):      
#         for protein in self.proteins:
#             #create charge environment class and load pdb file
#             chargeEnv = ChargeEnvironment()
#             path1 = os.path.join(self.folder, self.file_extension(protein,'pdb'))
#             chargeEnv.load_pdb(path1,protein)
            
#             #calculate charge environment
#             chargeEnv.calc_global_charge()
#             logging.debug("Total charge {} ({}+ & {}-)".format(chargeEnv.protein_charge,chargeEnv.plus_charge,chargeEnv.minus_charge))
#             chargeEnv.calc_charge_score()
#             #save modified pdb file
#             chargeEnv.save_pdb()
#             chargeEnv.save_csv()
    


    # BLOCK 2
    """
    Calculate labeling score
    """

    def calc_labeling_score(self):       
        weight_sum = 0
        for key, (weight,sens) in self.label_score_model.items(): weight_sum += float(weight)
        logging.info("Parameter weights {}".format(self.label_score_model))
        def save_csv(path,dictionary,header):
                with open(path, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for key, value in dictionary.items():
                        line = []
                        line.append(key)
                        for val in value: line.append(val)
                        writer.writerow(line)

        
        para_nbr = sum(x[0] > 0 for x in list(self.label_score_model.values()))
        for prot_idx,protein in enumerate(self.proteins):
            logging.info(protein)               
            label_params = {}
            set_AAkeys = []
            for key in self.label_score_model:
                path1 = os.path.join(self.folder, protein + r'_' + key + '.csv')
                if self.label_score_model[key][0]==0:
                    continue
                with open(path1, 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    label_params[key] = dict(reader)
                set_AAkeys.extend(label_params[key].keys())
            #take all occuring AAkeys in one list and sort list
            set_AAkeys = list(set(set_AAkeys))
            set_AAkeys.sort(key=lambda AAkey: AAkey[0] + "{:5d}".format(int(AAkey[1:])))
            label_score = {}
            label_parameter_score = {}
            #for AAkey in label_params[list(label_params.keys())[0]]:
            for AAkey in set_AAkeys:
                try:
                    score = 0
                    parameters = []
                    para_err = False
                    score_zero = False #set labelling score zero if one parameter is zero
                    for key in self.label_score_model:
                        if self.label_score_model[key][0]==0:
                            continue
                        try:
                            if not para_err and float(label_params[key][AAkey])>=0:
                                if float(label_params[key][AAkey])==0:
                                    score_zero = True
                                parameters.append(label_params[key][AAkey])
                                score += float(self.label_score_model[key][0]/weight_sum)*float(label_params[key][AAkey])
                            else: #if error occured before: add value to parameters list, keep score -1
                                score = -1.0
                                parameters.append(label_params[key][AAkey])
                                para_err = True
                        except: #on error: set score and paramter in parameters to -1
                            score = -1.0
                            parameters.append(-1.0)
                            para_err = True 
                    if score_zero:
                        score = 0.0
                except: #set score to -1 and fill parameters list to normal length (also wit -1)
                    score = -1.0
                    logging.debug(len(parameters))
                    for i in range(len(parameters),para_nbr):
                        parameters.append(-1.0)
                parameters.append(score)
                label_parameter_score[AAkey] = parameters #keep all entries in long list
                if score>0: #TBD check if all values should be kept
                    # label_parameter_score[AAkey] = parameters
                    label_score[AAkey] = [score]
                    
            path1 = os.path.join(self.folder, self.file_extension(protein,'pdb'))
            parser = PDB.PDBParser(PERMISSIVE=1)
            structure = parser.get_structure(protein,path1)
            model=structure[0]
            for chain in model:
                    chainId = chain.get_id()
                    chainCombi = [self.chainCombination,self.chainCombination2][prot_idx]
                    if chainId not in chainCombi:
                        logging.debug("Skip chain {}".format(chainId))
                        for residue in chain:
                            for atom in residue:
                                atom.set_bfactor(-1)
                        continue
                    for residue in chain:
                        #TODO ACCELERATE CHAINS WHICH ARE NOT IN LIST
                        resId = residue.get_id()
                        try:
                            parameterKey=chain.get_id()+str(resId[1])                          
                            bFact = label_parameter_score[parameterKey][-1]
                            for atom in residue:
                                atom.set_bfactor(bFact)
                        except:
                            for atom in residue:
                                atom.set_bfactor(-1)  
        
            #save pdb with score
            if self.SAVE_PDB:
                filepath = os.path.join(self.folder, protein + r'_LS.pdb')
                with open(filepath, 'w') as f:
                    #warnings.simplefilter("ignore")
                    io=PDBIO()
                    io.set_structure(structure)
                    io.save(f)
            
            #save score
            header = str(self.label_score_model)
            path1 = os.path.join(self.folder, protein + r'_LS.csv')
            save_csv(path1,label_score,header)
            path1 = os.path.join(self.folder, protein + r'_LSlong.csv')
            save_csv(path1,label_parameter_score,header)
        
    # BLOCK 3
    """
    Calculate PIFE score
    """
    
    
    # BLOCK 4
    """
    Calculate FRET score
    """
#    from FRETScore import FRETScore
#    import os
    def calc_fret_score(self, foerster_radius=60, method="SIMPLE", off=8.0, save_AV=False,weights=True):
        if self.mode=='f':
            self.calc_fret_score_double(foerster_radius=foerster_radius, method=method, off=off, save_AV=save_AV,weights=weights)
        elif self.mode=='s': #single FRET (only one pdb file)
            self.calc_fret_score_single(foerster_radius=foerster_radius, method=method, off=off, save_AV=save_AV,weights=weights) # TBD
        else:
            pass
        
        
    def calc_fret_score_double(self, foerster_radius=60, method="SIMPLE", off=8.0, save_AV=False,weights=True):     
        fret = FRETScore()
        fret.set_foerster_radius(foerster_radius)
        fret.set_method(method)
        fret.set_offset_AV(off)
        fret.set_save_AV(save_AV)
        fret.set_fluorophore(self.fluorophore1, self.fluorophore2)
        fret.set_folder(self.folder)
        fret.set_weights(weights)
        
        #load calculated labeling scores
        #TBD check protein 1 and 2 (switched???)
        apo_path = os.path.join(self.folder, self.protein1 + '_LS.csv')
        holo_path = os.path.join(self.folder, self.protein2 + '_LS.csv')
        fret.load_labeling_score(apo_path, self.protein1,'apo')
        fret.load_labeling_score(holo_path, self.protein2,'holo')
        #load pdbs
        apo_pdb_path = os.path.join(self.folder, self.file_extension(self.protein1,'pdb'))
        holo_pdb_path = os.path.join(self.folder, self.file_extension(self.protein2,'pdb'))
        fret.load_pdb(apo_pdb_path,self.protein1,'apo')
        fret.load_pdb(holo_pdb_path,self.protein2,'holo')
        #calculate pairing score
        fret.calc_measurement_scores(self.chainCombination,self.chainCombination2)
        #export results
        fret.save_csv()
        fret.save_csv('long')
    
    # BLOCK 4 (a)
    """
    Calculate FRET score (SINGLE CONFORMATION)
    """
#    from FRETScore import FRETScore
#    import os
    def calc_fret_score_single(self, foerster_radius=60, method="SIMPLE", off=8.0, save_AV=False,weights=True):
        fret = FRETScore()
        fret.set_foerster_radius(foerster_radius)
        fret.set_method(method)
        fret.set_offset_AV(off)
        fret.set_fluorophore(self.fluorophore1, self.fluorophore2)
        fret.set_folder(self.folder)
        fret.set_weights(weights)
        

        #load calculated labeling scores        
        path = os.path.join(self.folder, self.protein1 + '_LS.csv')
        fret.load_labeling_score(path, self.protein1,'apo')
        #load pdbs
        # pdb_path = os.path.join(self.folder, self.protein1 + '.pdb')
        pdb_path = os.path.join(self.folder, self.file_extension(self.protein1,'pdb'))
        fret.load_pdb(pdb_path,self.protein1,'apo')
        #calculate pairing score
        fret.calc_measurement_scores_single(self.chainCombination)
        #export results
        fret.save_csv()
        fret.save_csv('long')

    def get_all_file_paths(self, directory): 
      
        # initializing empty file paths list 
        file_paths = [] 
      
        # crawling through directory and subdirectories 
        for root, directories, files in os.walk(directory): 
            for filename in files: 
                # join the two strings in order to form the full filepath. 
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath) 
      
        # returning all file paths 
        return file_paths         
      
    def zip_files(self): 
        # path to folder which needs to be zipped 
#        directory = './python_files'
      
        # calling function to get all file paths in the directory 
        file_paths = self.get_all_file_paths(self.folder) 
        logging.debug('%s files will be zipped:' % len(file_paths)) 
      
        # writing files to a zipfile 
        zip_path = os.path.join(self.folder, 'result.zip')
        with ZipFile(zip_path,'w') as zip: 
            # writing each file one by one 
            for file in file_paths:
                if file != zip_path:
                    head_tail = os.path.split(file) 
                    zip.write(file, head_tail[1])
                else:
                    logging.debug("Skip file")
            zip.close()
        logging.info('All files zipped successfully!')
        return zip_path
        


# HELPER FUNCTIONS
    #TBD change load_parameter to itereate only once through list
    def load_parameter(self,path):
        with open(path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            label_params = dict(reader)
            #convert values to float
            for key in label_params.keys():
                label_params[key] = float(label_params[key])
        return label_params
