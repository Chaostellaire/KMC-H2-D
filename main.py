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
    "GAMMA1_SHARE" : 0.95, #float, GAMMA1/GAMMA, share of GAMMA1, GAMMA2_share = 1-GAMMA1/GAMMA. To get back to dimensionnal values we just need to multiply by GAMMA.

    "a" : 1,
    "b" : 0.3,

    #~~ SIMULATION VARIABLES ~~
    "load a table" : False, #bool, need to select correct parameter to load correct table
    "steps" : 1000000, #int, step number for simulation, output is size steps+1 (storing starting (0,0) position)
    
    #~~ SAVING PROPERTIES ~~#
    "table save flag" : True,
    "saving type" : "npy" , #str, gives the format of saving of the tables. npy is recommanded #### "npy",  "dat", "txt"

    #~~ VISUALIZATION ~~
    "visu" : True, #bool 
    "fps"  : 12, #int
    "D_computation" : True, #bool
}


start = time()



if Parameters["load a table"] :
    L = np.load("GAMMA1_SHARE_{}/model{}_step_{}.npy".format(Parameters["GAMMA1_SHARE"],Parameters['Model'], Parameters["steps"]))
else:
    if Parameters["Model"] == 1:
        L = KMC.trajectory_1(Parameters)
        compute_time = time() - start
        print("computation of trajectory done at {}".format(compute_time))
        
    if Parameters["Model"] == 2:  
        L = np.array([sublist[0] for sublist in KMC.trajectory_2(Parameters)])
        compute_time = time() - start
        print("computation of trajectory done at {}".format(compute_time))

    if Parameters["table save flag"] :
        savs.save2file(Parameters,L)
        print("time to save : {}".format( time()-compute_time ))

if Parameters["visu"] :
    #visu.animate_simulation(L, Parameters)
    visu.Diffusion_plot(Parameters,L)
#check for D vallidity



if Parameters["D_computation"] : 
    D_computed = KMC.computeDiffusion_normalized(L,Parameters)

    if Parameters["Model"] == 1 :
        D_true = 1/4 * (Parameters["GAMMA1_SHARE"] + 2 * (1-Parameters["GAMMA1_SHARE"]))
    else :
        D_true = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"]))*(Parameters["a"]-2*Parameters["b"]**2)
    print("================================")
    print("Ds are : ")
    print("real value = {}  ||| computed value = {}".format(D_true, D_computed))
    print("Error :      {:.1%}".format(np.abs(D_true-D_computed)/D_true))













