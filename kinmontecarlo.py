"""
kinmontecarlo.py : Short for Kinetic Monte Carlo method, will hold the computation of the trajectory of the H atom.
Chaostellaire : Harmonie, 

TO DO : 
- Verify with the Professor if H can go towards -x
- make a cool visualisation of the H displacement

"""
import numpy as np


def init_parameters(Parameters : dict) -> None:
    global GAMMA1, GAMMA2
    GAMMA1 = Parameters["GAMMA1_SHARE"]
    GAMMA2 = 1-Parameters["GAMMA1_SHARE"] 
    

def trajectory_1(Parameters: dict) -> np.ndarray :
    trajectory_vector = np.zeros((Parameters["steps"]+1,2), dtype = int)
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
        else :
            # We choose to go in the <1 0> direction i.e., +xy -xy -x+y +x-y
            x_random, y_random = directions[1][np.random.choice(4)]
            trajectory_vector[current_step] = trajectory_vector[current_step-1] + [x_random, y_random]
        current_step += 1
    return trajectory_vector

def trajectory_2(Parameters: dict) -> np.ndarray :

    a = Parameters["a"]
    b = Parameters["b"]

    trajectory_vector = np.zeros((Parameters["steps"]+1,2,2), dtype = float)
    trajectory_vector[0] = [[b,0], [1,0]]
    current_step = 1

    while current_step<=Parameters["steps"]:

        current_position = trajectory_vector[current_step-1][0]
        current_direction = trajectory_vector[current_step-1][1]

        rdmvalue = np.random.rand()
        if rdmvalue < GAMMA1 :
            # We choose to jump by making a hopping between the two O atoms
            new_position = current_position + current_direction*(a-2*b)
            new_direction = -current_direction
        else :
            # We choose to jump by 90° rotating aroung the first neighboring O atom
            n = np.random.choice(2)
            if current_direction[0] == 0: 
                new_direction = [(-1)**n, 0] 
            else: 
                new_direction = [0, (-1)**n]
            new_position = current_position + (new_direction - current_direction)*b
        
        trajectory_vector[current_step] = [new_position, new_direction]            
        current_step += 1

    return trajectory_vector






