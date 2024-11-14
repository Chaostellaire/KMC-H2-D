# KMC-H2-D
Modelisation Project : 2D diffusion of a proton with kinetic Monte-Carlo

# Goal

The goal is to recover the Diffusion coefficient of the mouvement of the proton. We need to compute a trajectory and find the mean quadratic value of which D is proportional to : $< \big( x(t_0+t) - x(t_0) \big) > = 4Dt$

# Usage
required libraries are stored in REQUIREMENT.txt.

- __main.py__ : Countains the main program, program to run to get results. To change input you can modify the Parameters dictionnary defined there.
- __kinmontecarlo.py__ : Countains every computation process and trajectories function.
- __savings.py__ : module used to save and load tables in npy format mainly.
- __visualization.py__ : every plot and animation function, need save trajectories to work.

# Parameters 
- "Model" : **int**, model number can be either 1 for empty lattice or 2 for full oxygen lattice.
- "GAMMA" : **float**, value of $\Gamma_1+\Gamma_2$ used only for final results plotting (use 1 for normalized case).
- "GAMMA1_SHARE": **float**, must be between 0 and 1, is the normalized value of $\Gamma_1$.
- "a" : ***float**, lattice parameter, used for D computation and trajectory of case 2.
- "b" : ***float**, space between the hydrogen and the oxygen, used for D computation and trajectory of case 2.
- "Do sim": **bool**, will do trajectory computation, if False will not automatically load a trajectory or mean quadratic distance. Will automatically save the current computed trajectory
- "load": **bool**, needed to load a trajectory.
- "steps": **int**, must be positive non zero, steps number. 
- "number of trajectories": **int**, must be positive non zero, number of trajectories you want to compute and show.
- "D_t_computation": **bool**, computes mean quadratic distance values from which we can deduce D(t). Will automatically save results.
- "D_gamma_computation": **bool**, computes D values for GAMMA1_SHARE ranging from 0.05 to 0.95. Will bypass *Do sim*. Will automatically save results.
- "custom load" : **bool**, if you want to load values from a custom file name. The file  must still be in GAMMA1_SHARE_xxx/.
- "custom save" : **bool**, same for saving location.
- "load path" : **str**, custom load/save path.
- "saving type": **str**, can be "npy" for npy file type or "txt" for txt format.
- "animation": **bool**, will produce animation for the trajectory. It is strongly discouraged to animate a trajectory of more than 1k steps.
- "D_t_plot": **bool**, will plot mean quadratic distance as a function of time.
- "D_gamma_plot": **bool**, will plot D as a function of gamma.
- "D_t_terminal": **bool**, will do comparison in the terminal of found D values.
- "fps" : *int*, must be positive, fps for the animation.
