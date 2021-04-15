#Animation part of code 
#For line animation 
#For grid animation 
import numpy as np
import matplotlib.pyplot as plt


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
    
        
    












































































































































































