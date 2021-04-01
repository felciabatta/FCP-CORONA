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
                 pTravel=0.01, pQuarantine=0.2, city='City', pEndQuarentine=0.05):
        
        self.city = city
        self.width = width
        self.height = height
        
        self.pEndQuarentine = pEndQuarentine
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
        
        # susceptible becomes infected with infections around point on grid
        if status == 'S':
            if rand < self.updateProb(i,j):
                return 'I'
            else:
                return 'S'
            
        # infected person either recovers, quarentines, dies or stays infected
        elif status == 'I':
            
            if r.random() < self.pQuarantine:
                return 'Q'
            
            if rand < self.pDeath:
                return 'D'
            elif rand < self.pRecovery:
                return 'R'
            else:
                return 'I'
            
        # quarantined, can either become dead, recovered or remain in quarentine. if in quarentine the virus cannot spread.
        elif status == 'Q':
            if rand < self.pDeath:
                return 'D'
            #person quarentine is ended too early and they come out infected
            elif rand < self.pEndQuarentine:
                return 'I'
            elif rand < self.pRecovery:
                return 'R'
            else:
                return 'Q'
        
        
        # recovered but may not have antibodies and can be infected again
        elif status == 'R':
            # person can become suceptible again after infection
            if rand < self.pReinfection:
                return 'S'
            
            else:
                return 'R'
        
        # vaccinated however vacine can be ineffective and person can be vunerable to infection
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
        
        #If someone is infected they have a possibility of travelling to another city
        elif status == 'I':
            if rand < self.pTravel:
                return 'T'
            else:
                return 'I'
            
        #Probability of if travelled person will return    
        elif status == 'T':
            if rand < self.pTravel:
                return 'I'
            elif rand < self.pRecovery:
                return 'R'
            else:
                return 'T'
            
        
        
    

    def TravelCount(self):
        """ determines amount of travelled people in the grid at any one time"""
        #convert grid into a list of lists of person states
        Grid = [list(row) for row in self.gridState]
        
        #convert the list of lists into a list of states in the grid
        Statuses = []
        for row in Grid:
            Statuses += row
        
        TravelCount = Statuses.count('T')
        
        return TravelCount
        
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
        """for use in print function: prints current grid state"""
        return str(self.gridState)
        
    
    
        

class PopulationSim:
    """
    Creates a class used to show the different cities within the simulation and the random travelling between them
    """
    
    
    def __init__(self, pInfection = 0.5):
        self.Bristol = subPopulationSim(pInfection = pInfection)
        self.Cardiff = subPopulationSim(pInfection = pInfection)
        self.pInfectedbyTraveller = 0
        self.pInfection = pInfection
        
    def PopulationTravel(self):
        TravelledNum = self.Bristol.TravelCount() + self.Cardiff.TravelCount()
        GridPoints = self.Bristol.width * self.Bristol.height + self.Cardiff.width * self.Cardiff.height
        pInfectedbyTraveller = (TravelledNum / GridPoints) * self.pInfection
        return pInfectedbyTraveller


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


def simTest3(days, w = 10):   # This will show how the states will vary with no quarantine with no vaccination.
    bristol = subPopulationSim(w, w, 0.001, 0.5, 0.1, 0.005, 0.01, 0.0, 'Bristol', 0)
    bristol.randomInfection()
    print("DAY 0:")
    print(bristol.gridState)  # Initial grid state (effectively this is day 0)

    for day in range(days):
        bristol.updateSubPopulation()
        print(f"DAY {day + 1}:")
        print(f"{bristol.gridState} \n")  # grid state after x days
        t.sleep(1)

    # simTest3 offers a title for each day so that the view can easily recognise how long since the initial infection

def simTest4(days, w = 10):   # This will show how the states will vary with quarantine with no vaccination.
    bristol = subPopulationSim(w, w, 0.001, 0.5, 0.1, 0.005, 0.01, 0.2, 'Bristol', 0.05)
    bristol.randomInfection()
    print("DAY 0:")
    print(bristol.gridState)  # Initial grid state (effectively this is day 0)

    for day in range(days):
        bristol.updateSubPopulation()
        print(f"DAY {day + 1}:")
        print(f"{bristol.gridState} \n")  # grid state after x days
        t.sleep(1)











