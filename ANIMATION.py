#Animation part of code 
#For line animation 
#For grid animation 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
"creates a grid animation of suceptible, infected, recovered "
#Creates a grid of colours to be plotted 




def get_Colours (self):
    colour_grid = np.zeros((self.width,self.height,3),int)
    for status, statusLet in self.gridState :
       colour = self.Colours[status]
       colour_rgb = self.COLOURMAP_RGB[colour]
       colour_grid[self.state == statusLet] = colour_rgb
       return colour_grid
       


class GridAnimation:
  def init (self, axes, simulation):
      self.axes=axes
      self.simulation=simulation
      
      
      self.image = self.axes.imshow(colour_grid)
      self.axes.set_xticks([])
      self.axes.set_yticks([])

  def init(self):
        return self.update(0)

  def update(self, data):
        
        return[self.image]
      
        
       






class LineAnimation: 
    """Creates a line animation showing the changes in Suceptible, Infected, Recovered and Dead people"""
    
<<<<<<< HEAD
        
    














=======
    #Writing in Psuedo Code until function is created
    #Importing data from simulation.py
    def __init__(self, data, axes, duration, line):
        self.axes = axes
        self.line = line
        self.duration = duration
        self.Suceptible = [data.loc['Susceptible', 'Population']]
        self.Recovered = [data.loc['Recovered', 'Population'] + data.loc['Vaccinated', 'Population']]
        self.Infected = [data.loc['Infected', 'Population'] + data.loc['Quarantine', 'Population'] + data.loc['Travelled', 'Population']]
        self.Dead = [data.loc['Dead', 'Population']]
       
       
    def init(self):
        self.axes.set_xlim([0, self.duration])
        self.axes.set_ylim([0, 100])
       
    def update(self, data):
        #Adding the amount of people in the SIRD states
        self.Suceptible.append(data.loc['Susceptible', 'Population'])
        self.Recovered.append(data.loc['Recovered', 'Population'] + data.loc['Vaccinated', 'Population'])
        self.Infected.append(data.loc['Infected', 'Population'] + data.loc['Quarantine', 'Population'] + data.loc['Travelled', 'Population'])
        self.Dead.append(data.loc['Dead', 'Population'])
        
>>>>>>> 5953129fd253eed1ea2424ea9704261adf06b484






























































































































































