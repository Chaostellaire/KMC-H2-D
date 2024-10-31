import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from kinmontecarlo import MQV
import savings
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
    if Parameters["Model"] == 1:
        D_true = 1/4*(Parameters["GAMMA1_SHARE"]*1+(1-Parameters["GAMMA1_SHARE"])*2) 
    else :
        D_true = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])) * (Parameters['a']-2*Parameters['b'])**2
        
    #O(n²)
    n = trajectory_vector.shape[0]
    if Parameters["load mqv"] and Parameters["load traj"]:
        if Parameters["custom load"]:
            MQV_compute= np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_mqv.{Parameters['saving type']}")[0]
            taken_steps = np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_mqv.{Parameters['saving type']}")[1]
        else:
            MQV_compute= np.load("GAMMA1_SHARE_{}/model{}_step_{}_mqv.npy".format(Parameters["GAMMA1_SHARE"],Parameters['Model'], Parameters["steps"]))[0]
            taken_steps = np.load("GAMMA1_SHARE_{}/model{}_step_{}_mqv.npy".format(Parameters["GAMMA1_SHARE"],Parameters['Model'], Parameters["steps"]))[1]
    else :
        #taken_steps = np.linspace(100, n+1, 20, dtype = int)
        taken_steps = np.linspace(0.2*n,0.8*n,20, dtype = int)
        MQV_compute = np.array([MQV(trajectory_vector, k) for k in taken_steps])
        savings.save2file(Parameters,np.stack((MQV_compute,taken_steps), axis = 0),"mqv")
           #to print we multiply 4Dt where t is adimensional so : t = step_number
    MQV_true_table = [4*D_true*1,4*D_true*n]
    D_eff1 = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])) * (Parameters['a']**2-2*Parameters['a']*Parameters['b']+Parameters['b']**2)
    MQV_eff1_table = [4*D_eff1*1,4*D_eff1*n]
    D_eff2 = 1/4*Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])/(1+Parameters["GAMMA1_SHARE"])*Parameters['a']**2
    MQV_eff2_table = [4*D_eff2*1,4*D_eff2*n]


            
    
    fig, ax = plt.subplots(figsize = (16,9))
    ax.set_xlim(1,n)
    ax.plot([1,n], MQV_true_table, label ="Real <[x(t0-t)-x(t0)]²> value", color = "blue", 
            linestyle = "solid")
    #
    ax.plot(taken_steps,MQV_compute, label = "Computed <[x(t0-t)-x(t0)]²> value", color = 'red', 
            linestyle = "dotted", marker = "^")
    ax.plot([1,n],MQV_eff1_table, label = "Effective", color = 'forestgreen')
    ax.plot([1,n],MQV_eff2_table, label = "Effective", color = 'black')

    #
    ax.legend()
    if ["custom load"]:
        plt.savefig(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}")
    else :
        plt.savefig(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/model{Parameters['Model']}_step_{Parameters['steps']}")
    plt.show()
    
