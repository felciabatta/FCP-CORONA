import numpy as np
import numpy.random as r
import time as t
import pandas as pd


class subPopulationSim:
    """
    creates a 'sub-population' e.g. a city of people, 
    which can be updated each day to determine new status of each person
    """

    def __init__(self, width=5, height=5, pDeath=0.001,
                 pInfection=0.5, pRecovery=0.1, pReinfection=0.005,
                 pTravel=0.01, pQuarantine=0.15, city='City',
                 pEndQuarantine=0.05
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

        # define 'local area' of a i,j grid point
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
        # print(localGrid)
        # input('next')

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
        print(f"{data}\n------------------------------------------------")


        PopulationTotal = data['Population'].sum()
        print(f"Total population: {PopulationTotal}")

        PercentInfected = 100 * len(infected) / PopulationTotal
        PercentSusceptable = 100 * len(susceptable) / PopulationTotal
        PercentRecovered = 100 * len(recovered) / PopulationTotal
        PercentDead = 100 * len(dead) / PopulationTotal
        PercentVaccinated = 100 * len(vaccinated) / PopulationTotal
        PercentQuarantined = 100 * len(quarantined) / PopulationTotal
        PercentTravelled = 100 * len(travelled) / PopulationTotal

        data2 = pd.DataFrame([PercentInfected, PercentSusceptable, PercentRecovered, PercentDead,
                              PercentVaccinated, PercentQuarantined, PercentTravelled],
                             columns=["Population State Percentages (%)"],
                             index=['Percent Infected',
                                    'Percent Susceptable',
                                    'Percent Recovered',
                                    'Percent Dead',
                                    'Percent Vaccinated',
                                    'Percent Quarantined',
                                    'Percent Travelled'
                                    ])
        print(f"{data2}\n------------------------------------------------")

        return data
        return data2



    def __str__(self):
        """for use in print function: prints current grid state"""
        return str(self.gridState)




class populationSim:
    """
    simulates multiple subpopulations and people travelling between them
    """


    def __init__(self, N=5, pInfection = 0.5):
        self.Bristol = subPopulationSim(width=N, height=N, pInfection = pInfection)
        self.Cardiff = subPopulationSim(width=N, height=N, pInfection = pInfection)
        self.pInfectedByTraveller = 0
        self.pInfection = pInfection


    def populationTravel(self):
        """defines probabilty of being infected by traveller"""
        TravelledNum = self.Bristol.TravelCount() + self.Cardiff.TravelCount()
        GridPoints = self.Bristol.width*self.Bristol.height + self.Cardiff.width*self.Cardiff.height
        self.pInfectedByTraveller = (TravelledNum / GridPoints)*self.pInfection


    def updatePopulation(self):
        """assigns new traveller infection and updates each subpopulation"""
        self.populationTravel()

        self.Bristol.pInfectedByTraveller=self.pInfectedByTraveller
        self.Cardiff.pInfectedByTraveller=self.pInfectedByTraveller

        self.Bristol.updateSubPopulation()
        self.Cardiff.updateSubPopulation()


    def __str__(self):
        """for use in print function: prints all current grid states"""
        return 'Bristol:\n'+str(self.Bristol)+'\n\n'+'Cardiff:\n'+str(self.Cardiff)+'\n\n\n'


# MANUAL TEST FUNCTIONS ---------------------------------------------------------
"""can be run manually in interactive console, for testing code"""

def simTestInit():
    sim=subPopulationSim()
    sim.randomInfection(0.2)
    print(sim)
    sim.updateSubPopulation()
    print(sim)
    return sim

def simTestDays(days, N=5):
    sim=subPopulationSim(width=N, height=N)
    sim.randomInfection(0.05)
    print(sim.gridState)

    for day in range(days):
        sim.updateSubPopulation()
        print(sim)
        t.sleep(1)
    return sim

def simTestPop(days, N=10):
    sim=populationSim(N=N)
    sim.Bristol.randomInfection(pInitialInfection=0.1)

    for day in range(days):
        sim.updatePopulation()
        print(sim)
        t.sleep(1)
    return sim


def simTest3(days, w = 10):   # This will show how the states will vary with no quarantine with no vaccination.
    bristol = subPopulationSim(w, w, 0.001, 0.5, 0.1, 0.005, 0.01, 0.0, 'Bristol', 0)
    bristol.randomInfection()
    print("DAY 0:")
    print(bristol.gridState)  # Initial grid state (effectively this is day 0)
    bristol.collectData()

    for day in range(days):
        t.sleep(1)
        bristol.updateSubPopulation()
        print(f"DAY {day + 1}:")
        print(f"{bristol.gridState} \n")  # grid state after x days
        bristol.collectData()


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
    return subPopulationSim(w, w,pDeath, pInfection, pRecovery, pReinfection, pTravel, pQuarantine, city,
                            pEndQuarantine)


def customSimTest(days):  # Try out different options for the variables easily using this
    subPop = createSubPop()
    subPop.randomInfection()
    print("DAY 0:")
    print(subPop.gridState)  # Initial grid state (effectively this is day 0)
    subPop.collectData()
    for day in range(days):
        t.sleep(1)
        subPop.updateSubPopulation()
        print(f"DAY {day + 1}:")
        print(f"{subPop.gridState} \n")  # grid state after x days
        subPop.collectData()


simTest3(30, 18)

# RESEARCH ----------------------------------------------------------------------

# Only 1/5 of symptomatic people DON'T self isolate
# as of April 1st, 1/100 HAVE covid













