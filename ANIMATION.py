import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 


class Animation:
    """Animates simultion as a grid and line graph"""
    
    def __init__(self, simulation, duration):
        self.simulation = simulation
        self.duration = duration
        
        self.figure = plt.figure(figsize=(8, 4))
        self.gridAx = self.figure.add_subplot(1, 2, 1)
        self.gridLine, = self.gridAx.plot([],[], lw=2) #TEMP, will delete later
        self.lineAx = self.figure.add_subplot(1, 2, 2)
        self.GridAnimation= GridAnimation(simulation.get_Colours(),self.gridAx,simulation)
        self.LineAnimation = LineAnimation(simulation.collectData(), self.lineAx, 
                                           duration, self.simulation.populationSize)
    
    def show(self):
        animation = FuncAnimation(self.figure, self.update, init_func=self.init, 
                                  frames=self.duration, blit=True, interval=150)
        plt.show()
        
    def init(self):
        self.gridLine.set_data([0],[0])
        return self.LineAnimation.init()
        return self.GridAnimation.inti()
    
    def update(self, framenum):
        self.simulation.update()
        # grid update
        return self.LineAnimation.update(self.simulation.collectData())
        return self.GridAnimation.update(self.simulation.get_Colours())


class GridAnimation():
    """creates a grid animation of suceptible, infected, recovered, dead states"""
    
    def __init__(self, axes, simulation, colour_grid):
        self.axes=axes
      
        colour_grid=simulation.get_Colours()
      
        self.image = self.axes.imshow(colour_grid)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
    def init(self):
        
        return self.update(0), 
    

    def update(self,data):
        
        colour_grid = subPopulationSim().get_Colours()
        self.image=colour_grid
        return [self.image]
        
    


class LineAnimation: 
    """Creates a line animation of Suceptible, Infected, Recovered and Dead states"""

    # Writing in Psuedo Code until function is created
    # Importing data from simulation.py
    
    def __init__(self, data, axes, duration, populationSize):
        self.axes = axes
        self.duration = duration
        # NOTE will need a line for each state, just temporary
        self.lineS, = self.axes.plot([],[],lw=2) 
        self.lineR, = self.axes.plot([],[],lw=2)
        self.lineD, = self.axes.plot([],[],lw=2)
        self.lineI, = self.axes.plot([],[],lw=2)
        self.yLim=populationSize
        
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
        Line.append(self.lineI)
        return Line
    


'''
class animation():
    def __init__(self):
        self.comment = "initialise here"
        
    #NOTE: Not sure where this goes yet
    def get_Colours(self):
        # Creates a grid of colours to be plotted 
        colour_grid = np.zeros((self.width,self.height,3),int)
        for status, statusLet in self.gridState :
            colour = self.Colours[status]
            colour_rgb = self.COLOURMAP_RGB[colour]
            colour_grid[self.state == statusLet] = colour_rgb
            return colour_grid
'''
    
        
        
