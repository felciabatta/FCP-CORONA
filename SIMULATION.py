import numpy as np




class SubPopulationSim:
	def __init__(self, Width, Height, Pdeath, Pinfection, Precovery, Preinfection, Ptravel, Pquarantine, cityname):
		self.Width = Width
		self.Height = Height
		self.Pdeath = Pdeath
		self.Pinfection = Pinfection
		self.Precovery = Precovery
		self.Preinfection = Preinfection
		self.Ptravel = Ptravel
		self.Pquarantine = Pquarantine
		self.cityname = cityname
		self.day = 0
		self.state = np.zeros([Width, Height], int)







	









	












