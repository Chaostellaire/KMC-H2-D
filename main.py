"""
Main.py : file to launch to execute the program, will countain basic function and test for the moment
Chaostellaire : Harmonie, 

TO DO:
- turn this into CLI for easy modification of Parameters values
"""
import kinmontecarlo as KMC;
import visualization as visu

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import savings as savs
from time import time
import numpy as np


Parameters = {

    "Model" : 2,

    #~~ OVERALL SYSTEM PROPERTIES ~~
    
    "GAMMA" : 1, #float, dimensionnal value for GAMMAs. [Hz]
    "GAMMA1_SHARE" : 0.25, #float, GAMMA1/GAMMA, share of GAMMA1, GAMMA2_share = 1-GAMMA1/GAMMA. To get back to dimensionnal values we just need to multiply by GAMMA.
    "lattice parameter" : 3., #float, refers to a, usefull only to get dimensionnal numbers back.
    
    "a" : 1,
    "b" : 0.3,

    #~~ SIMULATION VARIABLES ~~
    "steps" : 100, #int, step number for simulation, output is size steps+1 (storing starting (0,0) position)
    
    #~~ SAVING PROPERTIES ~~#
    "table save flag" : True,
    "saving type" : ".npy" , #str, gives the format of saving of the tables. .npy is recommanded #### ".npy",  ".dat", ".txt"
    
    "steps" : 300, #int, step number for simulation, output is size steps+1 (storing starting (0,0) position)

    #~~ VISUALIZATION ~~
    "visu" : True, #bool 
    "fps"  : 12, #int
    "D_computation" : True, #bool
}


start = time()



L = KMC.trajectory(Parameters)
print("computation of trajectory done at {}".format(time() - start))

if Parameters["Model"] == 1:
    L = KMC.trajectory_1(Parameters)
if Parameters["Model"] == 2:  
    L = np.array([sublist[0] for sublist in KMC.trajectory_2(Parameters)])

if Parameters["table save flag"] :
    savs.save2file(Parameters,L)

if Parameters["visu"] :
    visu.animate_simulation(L, Parameters)

#check for D vallidity

visu.Diffusion_plot(Parameters,L)


"""
D_computed = KMC.computeDiffusion_normalized(L,Parameters)
D_computed = KMC.MQV(L,20) / 80
print("Ds are : ")
print("real value = {}  ||| computed value = {}".format(D_true, D_computed))
"""












