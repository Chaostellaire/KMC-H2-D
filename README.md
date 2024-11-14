# KMC-H2-D
Modelisation Project : 2D diffusion of a proton with kinetic Monte-Carlo

# Usage
required libraries are stored in REQUIREMENT.txt.

main.py : Countains the main program, program to run to get results. To change input you can modify the Parameters dictionnary defined in main.py
kinmontecarlo.py : Countains every computation process and trajectories function.
savings.py : module used to save and load tables in npy format mainly
visualization.py : every plot and animation function, need savec trajectories to work

# Parameters 
- "Model" : *int*, model number can be either 1 for empty lattice or 2 for full oxygen lattice.
- "GAMMA" : *float*, value of $\Gamma_1+\Gamma_2$ used only for final results plotting (use 1 for normalized case)
- "GAMMA1_SHARE": *float*, must be between 0 and 1, is the normalized value of $\Gamma_1$

