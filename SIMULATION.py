import numpy as np
import numpy.random as r



class SubPopulationSim(W, H, Pdeath, Precovery, Preinfiction, Ptravel, Pquarantine, cityname):
	self.W = W
	self.H = H
	self.Pdeath = Pdeath
	self.Precovery = Precovery
    
    
    
    
    
    def UpdatePerson(self, i, j, state):
        """update person after every single day putting them into a new state of the same date"""
        status = state[i, j]
        rand = r.random()
        if status == 'S':
            if rand < self.UpdatePinfection:
                return 'I'
            else:
                return 'S'
        elif status == 'I':
            if rand < self.Pdeath:
                return 'D'
            elif rand < self.Precovery:
                return recovered
        elif status == 'R':
            if rand < self.Preinfiction:
                return 'I'
            elif:
                return 'R'
        elif status == 'D':
            return 'D' 
        elif status == 'V'    
            if rand < self.Preinfiction:
                return 'I'
            elif:
                return 'R'
        elif status == 0:
            return 0 
            


	
	












