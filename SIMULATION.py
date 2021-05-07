import numpy as np
import numpy.random as r
import time as t
import pandas as pd
from math import inf
from ANIMATION import *
   
class subPopulationSim:
    """
    creates a 'sub-population' e.g. a city of people, 
    which can be updated each day to determine new status of each person
    """
    #Uses real world probabilites when it comes to infection, death and reinfection
    def __init__(self, width=5, height=5, pDeath=0.02087,
                 pInfection=0.3, pRecovery=0.1, pReinfection=0.001,
                 pTravel=0.03, pQuarantine=0.15, city='City',
                 pEndQuarantine=0.05, pVaccination = 0.0001
                 ):

        self.city = city
        self.width = width
        self.height = height

        self.pEndQuarantine = pEndQuarantine
        self.pDeath = pDeath
        self.pInfection = pInfection
        self.pRecovery = pRecovery
        self.pReinfection = pReinfection
        self.pTravel = pTravel
        self.pQuarantine = pQuarantine
        self.pInfectedByTraveller = 0
        self.pVaccination = pVaccination

        self.day = 0
        
        # NOTE this includes empty spaces, but mainly for y axis limits
        self.populationSize=width*height

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


    def randomVaccination(self):
        """randomly infect, with probability pInitialInfection"""

        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                if self.gridState[i,j] == 'S' and r.random() < self.pVaccination:
                    self.gridState[i,j] = 'V'


    def update(self, dayV = inf, updatedVaccination = None):
        """updates whole subpopulation"""

        # initialise updated grid 
        updatedGrid = self.gridState.copy()

        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                updatedGrid[i,j] = self.updateStatus(i,j)

        # update gridState
        self.gridState = updatedGrid
        
        # update day
        self.day += 1
        
        # vaccination probability increases after a certain day, if a new value is specified
        if self.day >= dayV and updatedVaccination:
            self.pVaccination = updatedVaccination


    def updateStatus(self, i, j):
        """determine new status of a person"""
        #!!! IMPORTANT: need to change so prob's don't overlap #!!!
        status = self.gridState[i, j]
        rand = r.random()

        # susceptible 
        # can be infected by surrounding people or infected travellers
        if status == 'S':

            if rand < self.updateProb(i,j):
                return 'I'
            else:
                return status

        # infected 
        # can recover, quarantine, die, travel or remain unchanged
        elif status == 'I':

            if rand < self.pDeath:
                return 'D'
            elif rand < self.pTravel:
                return 'T'
            elif rand < self.pRecovery:
                return 'R'
            elif r.random() < self.pQuarantine:
                return 'Q'
            else:
                return status

        # quarantined
        # can recover, die, end quarantine early or remain unchanged
        elif status == 'Q':

            if rand < self.pDeath:
                return 'D'
            elif rand < self.pEndQuarantine:
                return 'I'
            elif rand < self.pRecovery:
                return 'R'
            else:
                return status

        # recovered or vaccinated
        # may become susceptible again, or remain unchanged
        elif status == 'R' or status == 'V':
            if rand < self.pReinfection:
                return 'S'
            else:
                return status

        # infected traveller 
        # may return, recover or remain unchanged
        elif status == 'T':

            if rand < self.pTravel:
                return 'I'
            elif rand < self.pRecovery:
                return 'R'
            else:
                return status

        # dead or unoccupied grid point
        # remains unchanged
        elif status == 'D' or status == 'N':
            return status


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

        # define 'local area' of an i,j grid point
        if i == 0:
            iMin = 0
        else:
            iMin = i-1

        if j == 0:
            jMin = 0
        else:
            jMin = j-1

        iMax = i+2
        jMax = j+2

        tempGrid = self.gridState.copy()
        tempGrid[i,j] = None

        localGrid = [list(row) for row in tempGrid[iMin:iMax,jMin:jMax]]

        # gather and count infection status in local area
        localStatuses=[]
        for row in localGrid:
            localStatuses += row
        # print(localStatuses,'\n')
        localInfectedCount = localStatuses.count('I')

        # calculate combined infection probability: 1-probabilityNotInfected
        pCombinedInfection = 1-(1-self.pInfectedByTraveller)*(1-self.pInfection)**localInfectedCount

        return pCombinedInfection


    def collectData(self):
        """Counts number of people in each state, and displays in a table
           This will aid in creating line animation & plots"""
           
        susceptable = []
        infected = []
        recovered = []
        travelled = []
        quarantined = []
        dead = []
        vaccinated = []
        
        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                if self.gridState[i, j] == 'I':
                    infected += 'I'
                elif self.gridState[i, j] == 'S':
                    susceptable += 'S'
                elif self.gridState[i, j] == 'R':
                    recovered += 'R'
                elif self.gridState[i, j] == 'D':
                    dead += 'D'
                elif self.gridState[i, j] == 'T':
                    travelled += 'T'
                elif self.gridState[i, j] == 'Q':
                    quarantined += 'Q'
                elif self.gridState[i, j] == 'V':
                    vaccinated += 'V'

        data = pd.DataFrame(
            [len(susceptable), len(infected), len(recovered), len(dead), len(travelled), len(quarantined),
             len(vaccinated)],
            columns=["Population"], index=['Susceptible',
                                           'Infected',
                                           'Recovered',
                                           'Dead',
                                           'Travelling',
                                           'Quarantining',
                                           'Vaccinated'])
        
        PopulationTotal = len(infected) + len(susceptable) + len(recovered) + len(dead) + len(vaccinated) + len(
            quarantined) + len(travelled)
        # print(f"Total population: {PopulationTotal}")

        PercentInfected = 100 * len(infected) / PopulationTotal
        PercentSusceptable = 100 * len(susceptable) / PopulationTotal
        PercentRecovered = 100 * len(recovered) / PopulationTotal
        PercentDead = 100 * len(dead) / PopulationTotal
        PercentVaccinated = 100 * len(vaccinated) / PopulationTotal
        PercentQuarantined = 100 * len(quarantined) / PopulationTotal
        PercentTravelled = 100 * len(travelled) / PopulationTotal

        PercentData = pd.Series([PercentSusceptable, PercentInfected, PercentRecovered, PercentDead, PercentTravelled,
                           PercentQuarantined, PercentVaccinated], name='Population State Percentages (%)',
                          index=['Susceptible',
                                   'Infected',
                                   'Recovered',
                                   'Dead',
                                   'Travelling',
                                   'Quarantining',
                                   'Vaccinated'])
        
        data['(%)'] = PercentData
        
        return data


    def __str__(self):
        """for use in print function: prints current grid state"""
        return str(self.gridState)

    
    def get_Colours (self):
        """For use in grid Animation gets a colour grid to be plotted"""
        
        colour_grid = np.zeros((self.width,self.height,3),int)
        for i in range(len(self.gridState)):
          for j in range(len(self.gridState[i])):
             if  self.gridState[i, j] == 'S':
                colour_grid[i][j][0]=0
                colour_grid[i][j][1]=255
                colour_grid[i][j][2]=0
             elif self.gridState[i, j] == 'I':
               colour_grid[i][j][0]=255
               colour_grid[i][j][1]=0
               colour_grid[i][j][2]=0
             elif self.gridState[i, j] == 'V':
               colour_grid[i][j][0]=0
               colour_grid[i][j][1]=0
               colour_grid[i][j][2]=255
             elif self.gridState[i, j] == 'D':     
                colour_grid[i][j][0]=0
                colour_grid[i][j][1]=0
                colour_grid[i][j][2]=0
             elif self.gridState[i, j] == 'Q': 
                colour_grid[i][j][0]=200
                colour_grid[i][j][1]=50
                colour_grid[i][j][2]=100
             elif self.gridState[i, j] == 'R': 
                colour_grid[i][j][0]=50
                colour_grid[i][j][1]=50
                colour_grid[i][j][2]=250
             elif self.gridState[i, j] == 'T': 
                colour_grid[i][j][0]=30
                colour_grid[i][j][1]=100
                colour_grid[i][j][2]=150
             elif self.gridState[i, j] == 'N': 
                colour_grid[i][j][0]=255
                colour_grid[i][j][1]=255
                colour_grid[i][j][2]=255
        
        return(colour_grid)
            

    


class populationSim:
    """
    simulates multiple subpopulations and people travelling between them
    """
    
    def __init__(self, subPopulations=[subPopulationSim(city="City1"),
                                       subPopulationSim(city="City2")], 
                 N=5, pInfection = 0.5):
        
        # initialise list of subpopulations, all have same pInfection,
        # all other parameters may be different
        self.subPopulations = subPopulations
        for sp in self.subPopulations:
            sp.pInfection = pInfection
        
        self.pInfectedByTraveller = 0
        self.pInfection = pInfection
        
        self.populationSize=0
        for sp in self.subPopulations:
            self.populationSize+=sp.populationSize
        


    def populationTravel(self):
        """defines probabilty of being infected by traveller"""
        TravelledNum = 0
        GridPoints = 0
        
        for sp in self.subPopulations:
            TravelledNum+=sp.TravelCount()
            GridPoints+=sp.populationSize
        
        self.pInfectedByTraveller = (TravelledNum / GridPoints)*self.pInfection


    def update(self):
        """assigns new traveller infection probabilty and updates each subpopulation"""
        self.populationTravel()
        
        for sp in self.subPopulations:
            sp.pInfectedByTraveller=self.pInfectedByTraveller
            sp.update()
    

    def collectData(self):
        data = pd.DataFrame(
            [0, 0, 0, 0, 0, 0, 0],
            columns=["Population"], index=['Susceptible',
                                           'Infected',
                                           'Recovered',
                                           'Dead',
                                           'Travelling',
                                           'Quarantining',
                                           'Vaccinated'])
        for sp in self.subPopulations:
            data += sp.collectData()
            
        return data






    def __str__(self):
        """for use in print function: prints all current grid states"""
        GridPrint=''
        for sp in self.subPopulations:
            GridPrint+=f'{sp.city}:\n'+str(sp)+'\n\n'
            
        # OLD CODE:
        # return 'Bristol:\n'+str(self.Bristol)+'\n\n'+'Cardiff:\n'+str(self.Cardiff)+'\n\n\n'
        
        return GridPrint


# MANUAL TEST FUNCTIONS ---------------------------------------------------------
"""can be run manually in interactive console for testing code, 
   or to be used in MAIN"""

def simTestInit():
    sim=subPopulationSim()
    sim.randomInfection(0.2)
    print(sim)
    sim.update()
    print(sim)
    return sim

def simTestDays(days, N=5):
    sim=subPopulationSim(width=N, height=N)
    sim.randomInfection(0.05)
    print(sim.gridState)

    for day in range(days):
        sim.update()
        print(sim)
        t.sleep(1)
    return sim

def simTestPop(days):
    cities = [subPopulationSim(15,15,city="London"),
            subPopulationSim(8,8,city="Bristol"),
            subPopulationSim(8,8,city="Manchester")]
    sim = populationSim(subPopulations=cities)
    sim.subPopulations[0].randomInfection(pInitialInfection=0.1)
    print("DAY: 0")
    print(sim)
    sim.collectData()
    t.sleep(1)

    for day in range(days):
        sim.update()
        print(f'DAY {day + 1}:')
        print(sim)
        sim.collectData()
        t.sleep(1)
    return sim


def simTest3(days, w = 10):
    # This will show how the states will vary with no quarantine with no vaccination.
    bristol = subPopulationSim(w, w, 0.001, 0.5, 0.1, 0.005, 0.01, 0.0, 'Bristol', 0)
    bristol.randomInfection()
    print("DAY 0:")
    print(bristol.gridState)  # Initial grid state (day 0)
    print(bristol.collectData())

    for day in range(days):
        t.sleep(1)
        bristol.update()
        print(f"DAY {day + 1}:")
        print(f"{bristol.gridState} \n")  # grid state after x days
        print(bristol.collectData())
        t.sleep(0.1)



def simTest4(days, w = 10):   # This will show how the states will vary with quarantine with no vaccination.
    bristol = subPopulationSim(w, w, 0.001, 0.5, 0.1, 0.005, 0.01, 0.2, 'Bristol', 0.05)
    bristol.randomInfection()
    print("DAY 0:")
    print(bristol.gridState)  # Initial grid state (effectively this is day 0)
    print(bristol.collectData())
    for day in range(days):
        bristol.update()
        print(f"DAY {day + 1}:")
        print(f"{bristol.gridState} \n")  # grid state after x days
        print(bristol.collectData())
        t.sleep(1)



def createSubPop():
    w = int(input("Input the width of the population size for a\n 'w x w' grid: "))
    pDeath = float(input("Input the probability of death from the virus: "))
    pInfection = float(input("Input the probability of infection from the virus: "))
    pRecovery = float(input("Input the probability of recovery for a infected person: "))
    pReinfection = float(input("Input the probability of getting re-infected\nafter already recovering: "))
    pTravel = float(input("Input the probability of the person travelling: "))
    pQuarantine = float(input("Input the probability of a person going into quarantine: "))
    city = input("Input the name of the city for the sub-population: ")
    pEndQuarantine = float(input("Input the probability of the person ending the quarantine early: "))
    return subPopulationSim(w, w, pDeath, pInfection, pRecovery, pReinfection, pTravel, pQuarantine, city,
                            pEndQuarantine)


def customSimTest(days):
    # Try out different options for the variables easily using this
    subPop = createSubPop()
    subPop.randomInfection()
    print("DAY 0:")
    print(subPop.gridState)  # Initial grid state (day 0)
    subPop.collectData()
    for day in range(days):
        t.sleep(1)
        subPop.update()
        print(f"DAY {day + 1}:")
        print(f"{subPop.gridState} \n")  # grid state after x days
        print(subPop.collectData())


def SimTestVaccine(days):
    """The probability of a person being vaccinated starts off as very rare, then increases as time goes on to a maximum of 10% """
    subPop = subPopulationSim(pVaccination = 0.0005, width = 15, height = 15)
    subPop.randomInfection()
    print("DAY 0:")
    print(subPop.gridState) 
    subPop.collectData()
    for day in range(days):
        if subPop.pVaccination < 0.01:
            subPop.pVaccination = subPop.pVaccination * 1.05
        subPop.randomVaccination()    
        t.sleep(1)
        subPop.update()
        print(f"DAY {day + 1}:")
        print(f"{subPop.gridState} \n")  
        print(subPop.collectData())
        

def TestAnimation(days,w):
 sim = subPopulationSim(w, w, 0.001, 0.5, 0.1, 0.005, 0.01, 0.0, 'Bristol', 0)
 sim.randomInfection(0.05)
 sim.randomVaccination()
       
 for day in range(days):
     t.sleep(1)
     sim.update()
     ani=Animation(sim,10)
     ani.update(1)
     ani.show()


# RESEARCH ----------------------------------------------------------------------

# Only 1/5 of symptomatic people DON'T self isolate
# as of April 1st, 1/100 HAVE covid
