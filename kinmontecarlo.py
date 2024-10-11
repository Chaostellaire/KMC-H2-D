"""
kinmontecarlo.py : Short for Kinetic Monte Carlo method, will hold the computation of the trajectory of the H atom. 
Chaostellaire : Harmonie, 

TO DO : 
- Verify with the Professor if H can go towards -x
- make a cool visualisation of the H displacement

"""
import numpy as np
from typing import Tuple;


def trajectory(steps: int, GAMMA1: float) -> Tuple[np.ndarray, np.ndarray] :
    trajectory_vector = np.zeros((steps+1, 2), dtype = int)
    choices = np.zeros((steps,), dtype = int)
    current_step = 1 
    """
    We create the directions array that stores any possibilities with that diffusion mechanism, i.e 
    directions[0] -> <1 0>
    directions[1] -> <1 1>

    """
    directions = np.array([[(1,0),(0,1),(-1,0),(0,-1)], [(1,1),(1,-1),(-1,1),(-1,-1)]])
    while current_step<=steps:
        rdmvalue = np.random.rand()
        if rdmvalue < GAMMA1 :
            # We choose to go in the <1 0> direction i.e., +x -x +y -y
            x_random, y_random = directions[0][np.random.choice(4)]
            trajectory_vector[current_step] = trajectory_vector[current_step-1] + [x_random, y_random]
            choices[current_step-1] = 1
        else :
            # We choose to go in the <1 0> direction i.e., +xy -xy -x+y +x-y
            x_random, y_random = directions[1][np.random.choice(4)]
            trajectory_vector[current_step] = trajectory_vector[current_step-1] + [x_random, y_random]
            choices[current_step-1] = 2
        current_step += 1
    return trajectory_vector, choices








