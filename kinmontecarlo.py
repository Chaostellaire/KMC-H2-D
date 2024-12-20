"""
kinmontecarlo.py : Short for Kinetic Monte Carlo method, will hold the computation of the trajectory of the H atom. 
DOES ONLY COMPUTATIONS.
Chaostellaire : Harmonie, 

TO DO :     
- make a cool visualisation of the H displacement

"""
import numpy as np
from time import time


    

def trajectory_1(Parameters: dict) -> np.ndarray :
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
        if rdmvalue < Parameters["GAMMA1_SHARE"] :
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
    return Parameters["a"]*trajectory_vector

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
        if rdmvalue < Parameters["GAMMA1_SHARE"] :
            # We choose to jump by making a hopping between the two O atoms
            new_position = current_position + current_direction *(a-2*b)
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


def MQV(trajectory_vector : np.ndarray, k_step:int) -> float :
    """
    compute the mean square norm between two H positions
    
    trajectory_vector is the H trajectory,
    k_step is related to t = k_step * dt
    """
    start = time()
    print("I'm at step {}".format(k_step))
    n = trajectory_vector.shape[0]
    result_MQV = 0
    for j_step in range(n - k_step) :
        position_diff = trajectory_vector[j_step+k_step] - trajectory_vector[j_step]
        result_MQV += np.dot(position_diff, position_diff)
    print("I finished in {}".format(time()-start))
    return result_MQV/(n-k_step)

def MQV_table(trajectory_vector:np.ndarray, taken_steps:np.ndarray) -> None :
    MQV_compute = np.array([MQV(trajectory_vector, k) for k in taken_steps])
    return MQV_compute


def computeDiffusion_normalized(trajectory_vector:np.ndarray, taken_steps: np.ndarray) -> float:
    """
    Computes a mean value of D/Gamma we need to recover : D = 1/4 (Gamma1 d1² + Gamma2 d2²)
    """
    D_storage = 0.0
    # We take only a few points to faster the computation speed, bc we know that we should get a linear asymptot
    # We also exclude the first 20%, because at low time scales the hydrogen didn't mooved that much across the lattice
    # We exclude the last 20% because they have too less point to compute a statifying mean
    for k_step in taken_steps:
        D_storage += MQV(trajectory_vector, k_step) / (4*k_step)
    return D_storage / taken_steps.size





