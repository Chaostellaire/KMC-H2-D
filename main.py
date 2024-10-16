"""
Main.py : file to launch to execute the program, will countain basic function and test for the moment
Chaostellaire : Harmonie, 

TO DO:
- (Object branch) turn Paramets into a class, easy feed
- turn this into CLI for easy modification of Parameters values
"""
import kinmontecarlo as KMC;
import visualization as visu

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.animation as animation


Parameters = {
    #~~ OVERALL SYSTEM PROPERTIES ~~
    
    "GAMMA" : 1, #float, dimensionnal value for GAMMAs. [Hz]
    "GAMMA1_SHARE" : 0.5, #float, GAMMA1/GAMMA, share of GAMMA1, GAMMA2_share = 1-GAMMA1/GAMMA. To get back to dimensionnal values we just need to multiply by GAMMA.
    "lattice parameter" : 3., #float, refers to a, usefull only to get dimensionnal numbers back.
    
    #~~ SIMULATION VARIABLES ~~
    "steps" : 100, #int, step number for simulation, output is size steps+1 (storing starting (0,0) position)
    
    
    #~~ SAVING PROPERTIES ~~#
    "table save flag" : True,
    "saving type" : ".npy" , #str, gives the format of saving of the tables. .npy is recommanded #### ".npy",  ".dat", ".txt"
    "table save path" : "./saves/tables/" , #path
    
    
    

    #~~ VISUALIZATION ~~
    "visu" : True, 
    "fps"  : 12,
}



KMC.init_parameters(Parameters)
L = KMC.trajectory(Parameters)

visu.animate_simulation(L, Parameters)












