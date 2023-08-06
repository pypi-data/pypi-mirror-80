# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:52:03 2017

@author: LAdmin
"""

from .LabelingParameter import LabelingParameter

class ConservationCopy(LabelingParameter):
    #constants / parameter
    file_tag = 'With_Conservation_Scores'
    #class variables
    
    def copy_conservation_score(self,chainOrigin,chainCopy):
        chainO=self.model[chainOrigin]
        chainC=self.model[chainCopy]
        for residue in chainO:
            resId = residue.get_id()
            try:
                bFact = residue.get_atoms().next().get_bfactor()
                for atom in chainC[resId]:
                    atom.set_bfactor(bFact)
            except:
                pass                  


class PDBOperation(LabelingParameter):
    #constants / parameter
#    file_tag = 'With_Conservation_Scores'
    #class variables
    
    def set_chain(self,chainName):
        for chain in self.model:
            print("Chain: <"+str(chain)+">")
#            chain.id = chainName
            self.rename_chain(chain.id,chainName)
            
    def rename_chain(self,oldChain, newChain):
        chain = self.model[oldChain]
        try:
            chain.id = newChain
        except:
            print("New chain <"+newChain+"> already exists. Chains will be merged.")
            chainGoal = self.model[newChain]
            for residue in chain:
                chainGoal.add(residue)
            self.model.detach_child(oldChain)
            
        