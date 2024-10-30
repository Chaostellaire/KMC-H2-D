import numpy as np
import matplotlib.pyplot as plt
import time

Parameters = {

    "Model" : 2,

    #~~ OVERALL SYSTEM PROPERTIES ~~
    
    "GAMMA" : 1, #float, dimensionnal value for GAMMAs. [Hz]
    "GAMMA1_SHARE" : 0.03, #float, GAMMA1/GAMMA, share of GAMMA1, GAMMA2_share = 1-GAMMA1/GAMMA. To get back to dimensionnal values we just need to multiply by GAMMA.

    "a" : 1,
    "b" : 0.3,

    #~~ SIMULATION VARIABLES ~~
    "load a table" : False, #bool, need to select correct parameter to load correct table
    "steps" : 10000000, #int, step number for simulation, output is size steps+1 (storing starting (0,0) position)
    
    #~~ SAVING PROPERTIES ~~#
    "table save flag" : True,
    "saving type" : "npy" , #str, gives the format of saving of the tables. npy is recommanded #### "npy",  "dat", "txt"

    #~~ VISUALIZATION ~~
    "animation" : False, #bool
    "D_plot" : True, #bool 
    "fps"  : 12, #int
    "D_computation" : True, #bool
}

a = Parameters["a"]
b = Parameters["b"]

plt.ion()
fig, ax = plt.subplots(figsize = (20,20))
ax.set_xlim(-11,11)
ax.set_ylim(-11,11)
atom, = ax.plot([], [], 'ro')

ax.set_xticks(range(-11, 11))
ax.set_yticks(range(-11, 11))
ax.grid(True)
ax.axhline(0, color='black',linewidth=0.5)
ax.axvline(0, color='black',linewidth=0.5)
current_position = np.array([b,0])
current_direction = np.array([1,0])
atom.set_data([b],[0])

step=0
while True:


    rdmvalue = np.random.rand()
    if rdmvalue < Parameters["GAMMA1_SHARE"] :
        # We choose to jump by making a hopping between the two O atoms
        current_position = current_position + np.multiply(a-2*b,current_direction)
        current_direction = np.multiply(-1,current_direction)
    else :
        # We choose to jump by 90° rotating aroung the first neighboring O atom
        n = np.random.choice(2)
        if current_direction[0] == 0: 
            new_direction = [(-1)**n, 0] 
        else: 
            new_direction = [0, (-1)**n]
        current_position = current_position + (np.subtract(new_direction, current_direction))*b #list - list unsupported ????
        current_direction = new_direction
    step += 1
    atom.set_data([current_position[0]], [current_position[1]])
    fig.canvas.draw()
    fig.canvas.flush_events()
    time.sleep(0.05)