#Animation part of code 
#For line animation 
#For grid animation 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

class GridAnimation:
   
       











class LineAnimation: 
    """Creates a line animation showing the changes in Suceptible, Infected, Recovered and Dead people"""
    
    #Writing in Psuedo Code until function is created
    def __init__(self, data, axes, duration, line):
        self.axes = axes
        self.line = line
        self.duration = duration
        self.Suceptible = [data.loc['Susceptible', 'Population']]
        self.Recovered = [data.loc['Recovered', 'Population'] + data.loc['Vaccinated', 'Population']]
        self.Infected = [data.loc['Infected', 'Population'] + data.loc['Quarantine', 'Population'] + data.loc['Travelled', 'Population']]
        self.Dead = [data.loc['Dead', 'Population']]
        
    def update(self, data):
        self.Suceptible.append(data.loc['Susceptible', 'Population'])
        self.Recovered.append(data.loc['Recovered', 'Population'] + data.loc['Vaccinated', 'Population'])
        self.Infected.append(data.loc['Infected', 'Population'] + data.loc['Quarantine', 'Population'] + data.loc['Travelled', 'Population'])
        self.Dead.append(data.loc['Dead', 'Population'])
        
    def 































































































































































