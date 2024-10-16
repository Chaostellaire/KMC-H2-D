"""
kinmontecarlo.py : Short for Kinetic Monte Carlo method, will hold the computation of the trajectory of the H atom. 
DOES ONLY COMPUTATIONS.
Chaostellaire : Harmonie, 

TO DO :     
- make a cool visualisation of the H displacement

"""
import numpy as np


def init_parameters(Parameters : dict) -> None:
    global GAMMA1, GAMMA2
    GAMMA1 = Parameters["GAMMA1_SHARE"]
    GAMMA2 = 1-Parameters["GAMMA1_SHARE"] 
    

def trajectory(Parameters: dict) -> np.ndarray :
    trajectory_vector = np.zeros((Parameters["steps"]+1,2), dtype = int)
    choices_vector = np.zeros((Parameters["steps"],), dtype = int )
    current_step = 1
    """
    We create the directions array that stores any possibilities with that diffusion mechanism, i.e 
    directions[0] -> <1 0>
    directions[1] -> <1 1>
    """
    directions = np.array([[(1,0),(0,1),(-1,0),(0,-1)], [(1,1),(1,-1),(-1,1),(-1,-1)]])
    while current_step<=Parameters["steps"]:
        rdmvalue = np.random.rand()
        if rdmvalue < GAMMA1 :
            # We choose to go in the <1 0> direction i.e., +x -x +y -y
            x_random, y_random = directions[0][np.random.choice(4)]
            trajectory_vector[current_step] = trajectory_vector[current_step-1] + [x_random, y_random]
            choices_vector[current_step-1] = 1
        else :
            # We choose to go in the <1 0> direction i.e., +xy -xy -x+y +x-y
            x_random, y_random = directions[1][np.random.choice(4)]
            trajectory_vector[current_step] = trajectory_vector[current_step-1] + [x_random, y_random]
            choices_vector[current_step-1] = 2
        current_step += 1
    return trajectory_vector


def MQV(trajectory_vector : np.ndarray, k_step:int) -> float :
    """
    compute the mean square norm between two H positions
    
    trajectory_vector is the H trajectory,
    k_step is related to t = k_step * dt
    """
    n = trajectory_vector.shape[0]
    result_MQV = 0.0
    for j_step in range(n - k_step) :
        position_diff = trajectory_vector[j_step+k_step] - trajectory_vector[j_step]
        result_MQV += np.dot(position_diff, position_diff)
    return result_MQV/(n-k_step)








