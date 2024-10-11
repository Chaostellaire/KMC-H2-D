"""
Main.py : file to launch to execute the program, will countain basic function and test for the moment
Chaostellaire : Harmonie, 

TO DO:
-  
"""
import kinmontecarlo as KMC;

Parameters = {
    #~~ OVERALL SYSTEM PROPERTIES ~~
    
    "GAMMA" : 1, #float, dimensionnal value for GAMMAs. [Hz]
    "GAMMA1_SHARE" : 0.5, #float, GAMMA1/GAMMA, share of GAMMA1, GAMMA2_share = 1-GAMMA1/GAMMA. To get back to dimensionnal values we just need to multiply by GAMMA.
    
    #~~ SIMULATION VARIABLES ~~
    "steps" : 100, #int, step number for simulation, output is size steps+1 (storing starting (0,0) position)
}



KMC.init_parameters(Parameters)
print(KMC.trajectory(Parameters)[70:100])




