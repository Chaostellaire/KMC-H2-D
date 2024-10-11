"""
Main.py : file to launch to execute the program, will countain basic function and test for the moment
Chaostellaire : Harmonie, 

TO DO:
- (Object branch) turn Paramets into a class, easy feed
- turn this into CLI for easy modification of Parameters values
"""
from simulation import Simulation;



simu = Simulation(1000, 0.5)
simu.run()
print(simu.H_path[70:100])




