Overview
========

File Structure
==============

MAIN.py

SIMULATION.py

PLOT.py

ANIMATION.py



Classes
=======

	SubPopulationSim(W, H, Pdeath, Precovery, Preinfiction, Ptravel, Pquarantine, cityname):
	"The grid of people with SIR, location and probability states"	
	
    	__init__(grid size, initial infected, inital vaccinated, initial empty):
    	
    	self.size = grid size
    	self.grid = Initialise grid with all Susceptible (np.zeros)
    	self.day = 0
    	- probability of someone 'leaving the grid' and infecting another grid
    	self.vaccinated = ??
        
        initialinfection(num)
        
        emptyspace():
        'randomly select grid points to be empty'
        
        vaccinate():
        'randomly vaccinate num of people'
        - V for vaccinated
        
    	updatePopulation():
    	'determines SIR states after t+=1 day'
    	- loops through every point on grid, and changes SIR status based on
        	 adjacent points, using updatePerson()
    	
    	
    	updatePerson():
    	'updates a single grid point'
    	- if infected, either recover, else: die, or stay infected
    	- if susceptible, probability of being infected depends on adjacent points, and other population
            - use indexing to determine status of adjacent point 
        - the grid point takes new value S,I,R,D,Q
        
        updateProbability:
            - To index and find probability of infection for partcular point

    PopulationSim(cityNum, cityNames):
    
    
    GridPlot()
	
	
	LinePlot()
	
    
    Animation():
    'combines different animations together'
        __init__:
        self.fig = create figure
        self.axes = create axes
        
        
    
    
    GridAnimation(SubPopulationSim)
    
        __init__:
        self.size = SubPopulationSim.size
        self.grid = SubPopulationSim.grid
        self.day = 
    

	LineAnimation()
	
	
	
	
    
    


Functions
=========

Arguments
=========

import argsparse

define all our arguments:
    size (NxN)
    probabilities


