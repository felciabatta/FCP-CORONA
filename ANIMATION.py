#Animation part of code 
#For line animation 
#For grid animation 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

class GridAnimation:
  def init (self, axes, simulation):
      self.axes=axes
      self.simulation=simulation
      
      rgb_matrix = self.simulation.get_sim.gridState
      self.image = self.axes.imshow(rgb_matrix)
      self.axes.set_xticks([])
      self.axes.set_yticks([])

  def init(self):
        return self.update(0)

  def update(self, framenum):
        day = framenum
        rgb_matrix = self.simulation.get_rgb_matrix()
        self.image.set_array(rgb_matrix)
        return [self.image]
        print(self.image)
      
        
       






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






























































































































































