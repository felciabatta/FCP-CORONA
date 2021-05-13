import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 


class Animation:
    """Animates simultion as a series of grids and single (combined) line graph
       Note: 'simulation' MUST be a populationSim class
    """
    
    def __init__(self, simulation, duration):
        self.simulation = simulation
        self.duration = duration
        
        # determines grid dimensions
        if len(simulation.subPopulations)<=3:
            cols = len(simulation.subPopulations)+1
            rows = 1
        else:
            cols = 4
            rows = int(np.ceil( (len(simulation.subPopulations)+1)/4 ))
        
        # figure sie depends on no. of sets of axes
        self.figure = plt.figure(figsize=(4*cols, 4*rows))
        
        # lineaimation axes
        self.lineAx = self.figure.add_subplot(rows, cols, (1,1))
        
        # creates as many sets of grid axes as no. of cities
        self.gridAxs = []
        for i in range(len(simulation.subPopulations)):
            self.gridAxs.append(self.figure.add_subplot(rows, cols ,i+2))
        
        # reduce empty space
        self.figure.tight_layout()
        
        # lineanimation of total SIRD across population
        self.LineAnimation = LineAnimation(simulation.collectData(), self.lineAx, 
                                           duration, self.simulation.populationSize)
        
        # gridanimation of each city
        self.GridAnimations = []
        for i in range(len(simulation.subPopulations)):
            self.GridAnimations.append(GridAnimation(self.gridAxs[i],simulation.subPopulations[i],
                                                     simulation.subPopulations[i].get_Colours()))
    
    
    def show(self):
        animation = FuncAnimation(self.figure, self.update, init_func=self.init, 
                                  frames=range(self.duration), blit=True, interval=200)
        
        plt.show()
        
    
    def save(self, filename = "CoronaSim.mp4", speed=200):
        animation = FuncAnimation(self.figure, self.update, init_func=self.init, 
                                  frames=range(self.duration), blit=True, interval=speed)
        
        animation.save(filename, dpi=300)
        
        
    def init(self):
        actors=[]
        
        actors+=self.LineAnimation.init()
        
        for ani in self.GridAnimations:
            actors+=ani.init()
        
        return actors
    
    
    def update(self, framenum):
        self.simulation.update()
        
        actors=[]
        
        actors+=self.LineAnimation.update(self.simulation.collectData())
        
        for ani in self.GridAnimations:
            actors+=ani.update(framenum)
            
        return actors
    

    
class animateIndividual:
    """Animates simultion as a grid and line graph
       One grid and line graph per subpopulation
       Note: 'simulation' MUST be a populationSim class
    """
    
    def __init__(self, simulation, duration):
        self.simulation = simulation
        self.duration = duration
        
        # figure sie depends on no. of sets of axes
        self.figure = plt.figure(figsize=(3*len(simulation.subPopulations), 6))
        
        # creates as many sets of line axes as no. of cities
        self.lineAxs = []
        for i in range(len(simulation.subPopulations)):
            self.lineAxs.append(self.figure.add_subplot(2,len(simulation.subPopulations),
                                                        len(simulation.subPopulations)+i+1))
        
        # creates as many sets of grid axes as no. of cities
        self.gridAxs = []
        for i in range(len(simulation.subPopulations)):
            self.gridAxs.append(self.figure.add_subplot(2,len(simulation.subPopulations),i+1))
        
        # reduce empty space: MAYBE NOT BEST FOR THIS LAYOUT, IT CUTS STUFF OFF
        # self.figure.tight_layout()
        
        # lineanimation of SIRD for each city
        self.LineAnimations = []
        for i in range(len(simulation.subPopulations)):
            self.LineAnimations.append(LineAnimation(simulation.subPopulations[i].collectData(), 
                                                     self.lineAxs[i], duration, 
                                                     self.simulation.subPopulations[i].populationSize))
        
        # gridanimation of each city
        self.GridAnimations = []
        for i in range(len(simulation.subPopulations)):
            self.GridAnimations.append(GridAnimation(self.gridAxs[i],simulation.subPopulations[i],
                                                     simulation.subPopulations[i].get_Colours()))     
    
    
    def show(self):
        animation = FuncAnimation(self.figure, self.update, init_func=self.init, 
                                  frames=range(self.duration), blit=True, interval=200)
        
        plt.show()
        
        
    def save(self, filename = "CoronaSim.mp4", speed=200):
        animation = FuncAnimation(self.figure, self.update, init_func=self.init, 
                                  frames=range(self.duration), blit=True, interval=speed)
        
        animation.save(filename, dpi=300)
        
        
    def init(self):
        actors=[]
        
        for ani in self.LineAnimations:
            actors+=ani.init()
        
        for ani in self.GridAnimations:
            actors+=ani.init()
        
        return actors
    
    
    def update(self, framenum):
        self.simulation.update()
        
        actors=[]
        
        for i in range(len(self.LineAnimations)):
            actors+=self.LineAnimations[i].update(self.simulation.subPopulations[i].collectData())
        
        for ani in self.GridAnimations:
            actors+=ani.update(framenum)
            
        return actors



class GridAnimation():
    """creates a grid animation of suceptible, infected, recovered, dead states"""
    
    def __init__(self, axes, simulation, colour_grid):
        self.axes=axes
        self.axes.set_title(simulation.city)
        
        self.simulation=simulation
        colour_grid=simulation.get_Colours()
        
        self.image = self.axes.imshow(colour_grid)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        
        
    def init(self):
        return self.update(0)
    
    
    def update(self, framenum):
        day = framenum
        colour_grid = self.simulation.get_Colours()
        self.image.set_array(colour_grid)
        return [self.image]
        
    

class LineAnimation: 
    """Creates a line animation of Suceptible, Infected, Recovered and Dead states"""
    
    def __init__(self, data, axes, duration, populationSize):
        self.axes = axes
        self.duration = duration
        
        self.lineS, = self.axes.plot([],[],lw=2,label='Susceptible', color='green') 
        self.lineR, = self.axes.plot([],[],lw=2, label='Recovered', color='blue')
        self.lineD, = self.axes.plot([],[],lw=2, label='Dead', color='black')
        self.lineI, = self.axes.plot([],[],lw=2, label='Infected', color='red')
        
        self.yLim=populationSize
        
        self.axes.legend(fontsize=6, ncol=2, handlelength=0.5, framealpha=0.8, 
                         fancybox=True, frameon=True, borderpad=0.6, columnspacing=1.0)
        self.axes.set_xlabel('Day')
        self.axes.set_ylabel('People')
        self.axes.tick_params(axis='y', rotation=90, labelsize=7)
        self.axes.tick_params(axis='x', labelsize=8)
        
        # prepare x data
        self.days = [0]
        
        # prepare y data
        self.Susceptible = [data.loc['Susceptible', 'Population']]
        self.Recovered = [data.loc['Recovered', 'Population'] + data.loc['Vaccinated', 'Population']]
        self.Infected = [data.loc['Infected', 'Population'] + data.loc['Quarantining', 'Population'] + data.loc['Travelling', 'Population']]
        self.Dead = [data.loc['Dead', 'Population']]
       
    
    def init(self):
        """Initialise LineAnimation """
        self.axes.set_xlim([0, self.duration])
        self.axes.set_ylim([0, self.yLim])
        Line = []
        self.lineS.set_data([],[])
        self.lineR.set_data([],[])
        self.lineD.set_data([],[])
        self.lineI.set_data([],[])
        Line.append(self.lineS,)
        Line.append(self.lineR,)
        Line.append(self.lineD,)
        Line.append(self.lineI,)
        return Line
        
       
    def update(self, data):
        # Adding the amount of people in the SIRD states
        self.days.append(len(self.days))
        self.Susceptible.append(data.loc['Susceptible', 'Population'])
        self.Recovered.append(data.loc['Recovered', 'Population'] + data.loc['Vaccinated', 'Population'])
        self.Infected.append(data.loc['Infected', 'Population'] + data.loc['Quarantining', 'Population'] + data.loc['Travelling', 'Population'])
        self.Dead.append(data.loc['Dead', 'Population'])
        Line = []
        self.lineS.set_data(self.days, self.Susceptible)
        self.lineR.set_data(self.days, self.Recovered)
        self.lineD.set_data(self.days, self.Dead)
        self.lineI.set_data(self.days, self.Infected)
        Line.append(self.lineS,)
        Line.append(self.lineR,)
        Line.append(self.lineD,)
        Line.append(self.lineI,)
        return Line


