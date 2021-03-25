import numpy as np
import numpy.random as r
import time as t



class subPopulationSim:
    """
    creates a 'sub-population' e.g. a city of people, 
    which can be updated each day to determine new status of each person
    """
    
    def __init__(self, width=5, height=5, pDeath=0.001, 
                 pInfection=0.5, pRecovery=0.1, pReinfection=0.005, 
                 pTravel=0.01, pQuarantine=0.2, city='City'):
        
        self.city = city
        self.width = width
        self.height = height
        
        self.pDeath = pDeath
        self.pInfection = pInfection
        self.pRecovery = pRecovery
        self.pReinfection = pReinfection
        self.pTravel = pTravel
        self.pQuarantine = pQuarantine
        
        self.day = 0
        
        # initalise grid of statuses, with susceptible people
        self.gridState = np.full([width, height], 'S')


    def emptyLocation(self, pEmpty):
        """randomly make some grid points empty, with probability pEmpty"""
        
        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                if r.random() < pEmpty:
                    self.gridState[i,j] = None
                    # Note: numpy changes None to 'N'


    def randomInfection(self, pInitialInfection=0.01):
        """randomly infect, with probability pInitialInfection"""
        
        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                if self.gridState[i,j] == 'S' and r.random() < pInitialInfection:
                    self.gridState[i,j] = 'I'
        
        
    def randomVaccination(self, pVaccination=0.05):
        """randomly infect, with probability pInitialInfection"""
        
        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                if self.gridState[i,j] == 'S' and r.random() < pVaccination:
                    self.gridState[i,j] = 'V'
 
    
    def updateSubPopulation(self):
        """updates whole subpopulation"""
    
        # initialise updated grid 
        updatedGrid = self.gridState.copy()
    
        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                updatedGrid[i,j] = self.updateStatus(i,j)

        # update gridState
        self.gridState = updatedGrid
    
    def updateStatus(self, i, j):
        """determine new status of a person"""
        
        status = self.gridState[i, j]
        rand = r.random()
        
        # susceptible
        if status == 'S':
            if rand < self.updateProb(i,j):
                return 'I'
            else:
                return 'S'
            
        # infected
        elif status == 'I':
            
            if r.random() < self.pQuarantine:
                return 'Q'
            
            if rand < self.pDeath:
                return 'D'
            elif rand < self.pRecovery:
                return 'R'
            else:
                return 'I'
            
        # quarantined (i.e. infected but can't spread)
        elif status == 'Q':
            if rand < self.pDeath:
                    return 'D'
            elif rand < self.pRecovery:
                return 'R'
            else:
                return 'Q'
        
        
        # recovered
        elif status == 'R':
            # may become susceptible, i.e. immunity wears off
            if rand < self.pReinfection:
                return 'S'
            else:
                return 'R'
        
        # vaccinated
        elif status == 'V':
            # may become susceptible, i.e. immunity wears off
            if rand < self.pReinfection:
                return 'S'
            else:
                return 'V'
        
        # dead
        elif status == 'D':
            return 'D'
        
        # no one at this location
        elif status == 'N':
            return None
        
        
    def updateProb(self, i, j):
        """updates probility of person being infected, if susceptible"""  
        
        # define 'local area' of a i,j grid point
        if i==0:
            iMin=0
        else:
            iMin=i-1    
        
        if j==0:
            jMin=0
        else:
            jMin=j-1
            
        iMax=i+2
        jMax=j+2
        
        tempGrid = self.gridState.copy()
        tempGrid[i,j]=None
        
        localGrid = [list(row) for row in tempGrid[iMin:iMax,jMin:jMax]]
        # print(localGrid)
        # input('next')
        
        # gather and count infection status in local area
        localStatuses=[]
        for row in localGrid:
            localStatuses+=row
        # print(localStatuses,'\n')
        localInfectedCount = localStatuses.count('I')
        
        # calculate combined infection probability: 1-probabilityNotInfected
        pCombinedInfection = 1-(1-self.pInfection)**localInfectedCount
        
        return pCombinedInfection
    
    def __str__(self):
        return str(self.gridState)
        
        







# MANUAL TEST FUNCTIONS ---------------------------------------------------------
"""can be run manually in interactive console, for testing code"""

def simTest1():
    sim=subPopulationSim()
    sim.randomInfection(0.2)
    print(sim.gridState)
    sim.updateSubPopulation()
    print(sim.gridState)
    return sim

def simTest2(days, N=5):
    sim=subPopulationSim(width=N, height=N)
    sim.randomInfection(0.05)
    print(sim.gridState)
    
    for day in range(days):
        sim.updateSubPopulation()
        print(sim.gridState)
        t.sleep(1)
    return sim

	















