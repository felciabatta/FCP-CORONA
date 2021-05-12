import numpy as np
import numpy.random as r
import time as t
import pandas as pd
from ANIMATION import *


class person:
    
    def __init__(self, status="S"):
        
        self.status = status
        
        self.previouslyInfected = False
        self.quarantining = False
        self.vaccinated = False
        self.travelling = False
        
        self.initializeValues()
        
    def initializeValues(self):
        
        self.daysInfected = 0
        self.daysQuarantining = 0
        self.pQuarantine = 0.01
        self.pVaccinate = 0.01
        self.pTravel = 0.01
        self.pDeath = 0
        self.pRecovery = 0
        self.pEndQuarantine = 0
        
    def updateProbabilities(self):
        
        if self.status == "S":
            self.pInfection = self.neighbours.count("I") * 0.1
            
            if self.previouslyInfected:
                self.pVaccinate = 0.1
            
              
        elif self.status == "I":
            if self.daysInfected >= 4 :
                if self.daysInfected <= 10:
                    self.pDeath = (self.daysInfected - 3) * 0.01
                    self.pRecovery = (self.daysInfected - 3) * 0.01
                    self.pQuarantine = (self.daysInfected - 3) * 0.01
                else:
                    self.pDeath = 0.07
                    self.pRecovery = 0.07
                    self.pQuarantine = 0.07
                    
        if self.quarantining:
            if self.daysQuarantining >= 4 :
                if self.daysQuarantining <= 10:
                    self.pEndQuarantine = (self.daysQuarantining - 3) * 0.01
                else:
                    self.pEndQuarantine= 0.07
            
              
    def updateStatus(self):
        """determine new status of a person"""
        
        # susceptible 
        # can be infected by surrounding people or infected travellers
        if self.status == "S":
            
            if r.random() < self.pInfection:
                self.status = "I"
            
            elif r.random() < self.pVaccinate:
                self.vaccinated = True
            
            elif r.random() < self.pQuarantine:
                self.quarantining = True
                
        # infected 
        # can recover, quarantine, die, travel or remain unchanged
        elif self.status == "I":
            
            self.daysInfected += 1
            
            if r.random() < self.pRecovery:
                self.previouslyInfected = True
                self.status = "S"
            
            elif  r.random() < self.pDeath:
                self.status = "D"
                
            elif r.random() < self.pTravel:
                self.travelling = True
            

                
        # quarantined
        # can recover, die, end quarantine early or remain unchanged
        if self.quarantining:
            
            self.daysQuarantining += 1
            
            if r.random() < self.pEndQuarantine:
                self.quarantining = False
            
            
    def __str__(self):
        return self.status



class subPopulationSim:
    """
    creates a 'sub-population' e.g. a city of people, 
    which can be updated each day to determine new status of each person
    """

    def __init__(self, width=5, height=5, city='City'):

        self.city = city
        # self.width = width
        # self.height = height

        self.day = 0
        
        # NOTE this includes empty spaces, but mainly for y axis limits
        self.populationSize=width*height

        # initalise grid of statuses, with susceptible people
        self.gridState = [[person() for x in range(width)] for y in range(height)]


    def emptyLocation(self, pEmpty=0.1):
        """randomly make some grid points empty, with probability pEmpty"""

        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                if r.random() < pEmpty:
                    self.gridState[i][j] = None
                    # Note: numpy changes None to 'N'


    def randomInfection(self, pInitialInfection=0.05):
        """randomly infect, with probability pInitialInfection"""

        for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                if r.random() < pInitialInfection and type(self.gridState[i][j]) == person:
                    self.gridState[i][j].status = "I"
                    
                    
    def nextDay(self):
        """updates whole subpopulation"""
        
        self.identifyNeighbours()
        
        for i in self.gridState:
            for j in i:
                j.updateProbabilities()
                j.updateStatus()
                
        self.moveAround
        
        self.day += 1


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
    
    def moveAround(self, pMove):
        for i in self.gridState:
            for j in i:
                if r.random() < j.pMove:
                    j


    def identifyNeighbours(self):
        
       for i in range(len(self.gridState)):
            for j in range(len(self.gridState[i])):
                if type(self.gridState[i][j]) == person:
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
            
                    tempGrid = np.array(self.gridState)
                    # tempGrid[i,j] = None
            
                    localGrid = [list(row) for row in tempGrid[iMin:iMax,jMin:jMax]]
                   
    
            # gather and count infection status in local area
                    self.gridState[i][j].neighbours=[]
                    for row in localGrid:
                        self.gridState[i][j].neighbours += row
                    self.gridState[i][j].neighbours = [person.status for person in self.gridState[i][j].neighbours if person != None and not person.quarantining] 
               

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
                if self.gridState[i][j].status == 'I':
                    if self.gridState[i][j].previouslyInfected:
                        recovered += 'R'
                    else:
                        infected += 'I'
                elif self.gridState[i][j].status == 'S':
                    if self.gridState[i][j].previouslyInfected:
                        recovered += 'R'
                    else:
                        susceptable += 'S'
                elif self.gridState[i][j].status == 'D':
                    dead += 'D'
                elif self.gridState[i][j].status == 'T':
                    travelled += 'T'
                elif self.gridState[i][j].status == 'Q':
                    quarantined += 'Q'
                elif self.gridState[i][j].status == 'V':
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
        # NOTE: rather than printing within method, do nothing, so have option to
        #       print outside of method 
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



    def get_Colours (self):
        """For use in grid Animation gets a colour grid to be plotted"""
            
        colour_grid = np.zeros((self.width,self.height,3),int)
        for i in range(len(self.gridState)):
          for j in range(len(self.gridState[i])):
             if  self.gridState[i][j].status == 'S':
                 if self.gridState[i][j].previouslyInfected:
                     colour_grid[i][j][0]=50
                     colour_grid[i][j][1]=50
                     colour_grid[i][j][2]=250
                 else:
                    colour_grid[i][j][0]=0
                    colour_grid[i][j][1]=255
                    colour_grid[i][j][2]=0
             elif self.gridState[i][j].status == 'I':
                 # if self.gridState[i][j].previouslyInfected:
                 #    colour_grid[i][j][0]=50
                 #    colour_grid[i][j][1]=50
                 #    colour_grid[i][j][2]=250
                 # else:
                    colour_grid[i][j][0]=255
                    colour_grid[i][j][1]=0
                    colour_grid[i][j][2]=0
             elif self.gridState[i][j].status == 'V':
               colour_grid[i][j][0]=0
               colour_grid[i][j][1]=0
               colour_grid[i][j][2]=255
             elif self.gridState[i][j].status == 'D':     
                colour_grid[i][j][0]=0
                colour_grid[i][j][1]=0
                colour_grid[i][j][2]=0
             elif self.gridState[i][j].status == 'Q': 
                colour_grid[i][j][0]=200
                colour_grid[i][j][1]=50
                colour_grid[i][j][2]=100
             elif self.gridState[i][j].status == 'R': 
                colour_grid[i][j][0]=50
                colour_grid[i][j][1]=50
                colour_grid[i][j][2]=250
             elif self.gridState[i][j].status == 'T': 
                colour_grid[i][j][0]=30
                colour_grid[i][j][1]=100
                colour_grid[i][j][2]=150
        
        return(colour_grid)
    
    
    def __str__(self):
        """for use in print function: prints current grid state"""
        tempGrid = np.array(self.gridState)
        for i in range(len(tempGrid)):
            for j in range(len(tempGrid[i])):
                tempGrid[i][j] = str(tempGrid[i][j])
        return str(tempGrid)

            

class populationSim:
    """
    simulates multiple subpopulations and people travelling between them
    """


    def __init__(self, subPopulations=[subPopulationSim(city="City1"),
                                       subPopulationSim(city="City2")], 
                 pInfection = 0.5):
        
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
            sp.nextDay()
    

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







# x = subPopulationSim()
# x.randomInfection()
# for i in range(20):
#     x.nextDay()
#     print(x)
# print(x.gridState[1][2].pQuarantine, x.gridState[1][2].daysInfected, x.gridState[1][2].quarantining)

