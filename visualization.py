import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from kinmontecarlo import MQV
import os

def animate_simulation(L : np.ndarray, Parameters : dict) -> None:
        # Create the figure and axis
        print("HELLO")
        fig, ax = plt.subplots()

        # Set limits for the grid centered at (0, 0)
        x_min = min([x for x, y in L]) - 1
        x_max = max([x for x, y in L]) + 1
        y_min = min([y for x, y in L]) - 1
        y_max = max([y for x, y in L]) + 1

        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

        # Initialize the grid and atom position
        atom, = ax.plot([], [], 'ro')  # Red dot for the atom

        # Set grid lines
        m = round(min(x_min, y_min))-1
        M = round(max(x_max, y_max))+1
        ax.set_xticks(range(m, M + 1))
        ax.set_yticks(range(m, M + 1))
        ax.grid(True)

        # Add x and y axis lines crossing at (0, 0)
        ax.axhline(0, color='black',linewidth=0.5)
        ax.axvline(0, color='black',linewidth=0.5)

        # Initialization function
        def init():
            atom.set_data([], [])
            return atom,

        # Animation function
        def animate(i):
            x, y = L[i]
            atom.set_data([x], [y])
            return atom,

        # Initialize writer for saving the video
        writervideo = animation.FFMpegWriter(fps=Parameters['fps'])  # Ensure ffmpeg is installed

        # Create the animation
        ani = animation.FuncAnimation(fig, animate, frames=len(L), init_func=init, blit=True)
        
        # Save the animation
        directory_path = f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}"
        os.makedirs(directory_path, exist_ok=True)
        ani.save(f"{directory_path}/anim_steps{Parameters['steps']}_fps{Parameters['fps']}.mp4", writer=writervideo)

def Diffusion_plot(Parameters : dict, trajectory_vector : np.ndarray) -> None :
    D_true = (Parameters["GAMMA1_SHARE"]*1+(1-Parameters["GAMMA1_SHARE"])*2) 
    D_true_table = np.ones((Parameters["steps"],))* D_true
    #O(n²)
    n = trajectory_vector.shape[0]
    taken_steps = np.linspace(1, n, 100, dtype = int)
    #taken_steps = np.linspace(0.2*n,0.8*n,100, dtype = int)
    MQV_compute = [MQV(trajectory_vector, k) for k in taken_steps]
    D_moyen = np.ones((Parameters['steps']))* np.mean(np.divide(MQV_compute, taken_steps*4))
    #to print we multiply 4Dt where t is adimensional so : t = step_number
    steps_relevant = np.arange(1, n, 1)
    MQV_true_table = np.multiply(D_true_table, np.arange(1, n, 1))


    
    
    fig, ax = plt.subplots(figsize = (16,9))
    ax.set_xlim(1,n)
    ax.plot(np.arange(1, n, 1), MQV_true_table, label ="Real <[x(t0-t)-x(t0)]²> value", color = "blue", 
            linestyle = "solid")
    #
    ax.plot(taken_steps,MQV_compute, label = "Computed <[x(t0-t)-x(t0)]²> value", color = 'red', 
            linestyle = "dotted", marker = "^")
    #
    #ax.plot(D_moyen, label = "mean")
    #ax.set_ylim(0,max(D_moyen)*1.1)
    ax.legend()
    plt.show()
    
