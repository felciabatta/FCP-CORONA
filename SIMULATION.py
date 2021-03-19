import numpy as np
import numpy.random as r




class SubPopulationSim:
	def __init__(self, Width, Height, Pdeath, Pinfection, Precovery, Preinfection, Ptravel, Pquarantine, cityname):
		self.Width = Width
		self.Height = Height
		self.Pdeath = Pdeath
		self.Pinfection = Pinfection
		self.Precovery = Precovery
		self.Preinfection = Preinfection
		self.Ptravel = Ptravel
		self.Pquarantine = Pquarantine
		self.cityname = cityname
		self.day = 0
		self.state = np.zeros([Width, Height], int)

    
    
    
    
    
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
            
        
        


	









	















