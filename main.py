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
import os
import numpy as np


Parameters = {

    "Model" : 2,

    #~~ OVERALL SYSTEM PROPERTIES ~~
    
    "GAMMA" : 1, #float, dimensionnal value for GAMMAs. [Hz]
    "GAMMA1_SHARE" : 0.5, #float, GAMMA1/GAMMA, share of GAMMA1, GAMMA2_share = 1-GAMMA1/GAMMA. To get back to dimensionnal values we just need to multiply by GAMMA.

    "a" : 1,
    "b" : 0.3,

    #~~ SIMULATION VARIABLES ~~
    "Do sim" : False,
    "load traj" : False, #bool, need to select correct parameter to load correct table
    "load mqv": False, #bool, will trigger only if a trajectory load is prompted
    "custom load" : False, #bool, will trigger only if a trajectory load is prompted
    "custom save" : False, #bool, will use the structure ./GAMMA1/xxxxx
    "load path" :"M2_10M_2", #str
    
    "steps" : 10000000, #int, step number for simulation, output is size steps+1 (storing starting (0,0) position)
    "several trajectories": False, #bool, NOT IMPLEMENTED
    "number trajectories": 5, #int, NOT IMPLEMENTED
    "D_t_computation" : False, #bool
    "D_gamma_computation" : True, #bool

    
    
    #~~ SAVING PROPERTIES ~~#
    "table save flag" : True,
    "saving type" : "npy", #str, gives the format of saving of the tables. npy is recommanded #### "npy",  "dat", "txt"

    #~~ VISUALIZATION ~~
    "animation" : False, #bool
    "D_t_plot" : False, #bool 
    "D_gamma_plot": True, #bool
    "fps"  : 12, #int
    
    
}


start = time()



if Parameters["load traj"] :
    if Parameters["custom load"]:
        L = np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_traj.{Parameters['saving type']}")
    else:
        L = np.load("GAMMA1_SHARE_{}/model{}_step_{}_traj.npy".format(Parameters["GAMMA1_SHARE"],Parameters['Model'], Parameters["steps"]))
elif Parameters["Do sim"]:
    if Parameters["Model"] == 1:
        L = KMC.trajectory_1(Parameters)
        compute_time = time() - start
        print("computation of trajectory done at {}".format(compute_time))
        
    if Parameters["Model"] == 2:  
        L = KMC.trajectory_2(Parameters)[:,0]
        compute_time = time() - start
        print("computation of trajectory done at {}".format(compute_time))

    if Parameters["table save flag"] :
        savs.save2file(Parameters,L,"traj")
        print("time to save : {}".format( time()-compute_time ))


if Parameters["animation"] :
    visu.animate_simulation(L, Parameters)
if Parameters["D_t_plot"]:
    visu.Diffusion_plot(Parameters,L)


    
#check for D validity



if Parameters["D_t_computation"] : 
    if Parameters["load mqv"]:
        if Parameters["custom load"]:
            MQV_computed = np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_mqv.{Parameters['saving type']}")[0]
            taken_steps = np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_mqv.{Parameters['saving type']}")[1]
            D_computed = np.mean(np.divide(MQV_computed,taken_steps))
        else:
            MQV_computed = np.load("GAMMA1_SHARE_{}/model{}_step_{}_mqv.npy".format(Parameters["GAMMA1_SHARE"],Parameters['Model'], Parameters["steps"]))[0]
            taken_steps = np.load("GAMMA1_SHARE_{}/model{}_step_{}_mqv.npy".format(Parameters["GAMMA1_SHARE"],Parameters['Model'], Parameters["steps"]))[1]
            D_computed = np.mean(np.divide(MQV_computed,taken_steps))
    else:
        D_computed = KMC.computeDiffusion_normalized(L,Parameters)

    if Parameters["Model"] == 1 :
        D_true = 1/4 * (Parameters["GAMMA1_SHARE"] + 2 * (1-Parameters["GAMMA1_SHARE"]))*Parameters['a']**2
    else :
        D_true = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])) * (Parameters['a']-2*Parameters['b'])**2
        D_eff1 = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])) * (Parameters['a']**2-2*Parameters['a']*Parameters['b']+Parameters['b']**2)
        D_eff2 = 1/4*Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])/(1+Parameters["GAMMA1_SHARE"])*Parameters['a']**2
    print("================================")
    print("Ds are : ")
    print("real value = {}  ||| computed value = {}".format(D_true, D_computed))
    print("eff1 value = {}  ||| eff2 value = {}".format(D_eff1,D_eff2))
    print("Error :      {:.1%}".format(np.abs(D_true-D_computed)/D_true))
    print("Error eff1 : {:.1%}  ||| Error eff2 : {:.1%}".format(np.abs(D_computed-D_eff1)/D_computed,np.abs(D_computed-D_eff2)/D_computed))

print('==========================================')
if Parameters["D_gamma_computation"]:
    os.makedirs('D_gamma', exist_ok=True)

    #Table to store D
    gamma_table = np.arange(0.05,0.95,0.05)
    i = 0
    D_table = np.zeros_like(gamma_table)
    for gamma in gamma_table :
        Parameters["GAMMA1_SHARE"] = gamma
        print(f"Generating trajectory for GAMMA1 = {gamma}")
        if Parameters["Model"] == 1:
            L = KMC.trajectory_1(Parameters)        
        if Parameters["Model"] == 2:  
            L = KMC.trajectory_2(Parameters)[:,0]
        np.save(f"D_gamma/traj_{gamma:.3f}_{Parameters['steps']/100000}step",L)
        
        print("computing D")
        D_curr = KMC.computeDiffusion_normalized(L, Parameters)
        print(f"D = {D_curr}")
        D_table[i] = D_curr
        i+=1
        print("======================================")
    np.save('D_gamma/D_values', D_table)

if Parameters["D_gamma_plot"]:
    D_table = np.load("D_gamma/D_values.npy")
    gamma_table = np.arange(0.05,0.95,0.05)
    
    visu.Diffusion_gamma(gamma_table,D_table,Parameters)
        
        













