import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import numpy as np
from kinmontecarlo import MQV
import savings
import os

COMPUTED_COLOR = ["lightcoral", "tomato", "red", "firebrick", "maroon","peachpuff","gold","darkorange","peru","dark"]

def animate_simulation(Parameters : dict) -> None:
    #load table
    L = savings.loadtraj(Parameters)
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
    ani.save(f"{directory_path}/anim_steps{Parameters['steps']}_fps{Parameters['fps']}.gif", writer= "pillow")
    ani.save(f"{directory_path}/anim_steps{Parameters['steps']}_fps{Parameters['fps']}.mp4", writer= writervideo)
    
    

def Diffusion_time(Parameters: dict) -> None :
    fig,ax = plt.subplots(figsize = (18,10))
    color_choice = choose_color_computed(Parameters["number trajectories"])
    n = (Parameters['steps']+1)*0.001
    for i in range(1,Parameters["number trajectories"]+1):
        Parameters["current trajectory"] = i
        MQV_compute= savings.loadmqv(Parameters)[0]
        taken_steps = savings.loadmqv(Parameters)[1]
        
    
    
        ax.plot(taken_steps, MQV_compute,label = f"Computed <[x(t0-t)-x(t0)]²> value, traj{i}", color = color_choice[i], 
        linestyle = "dashed", marker = "^")
    #end for
    n = taken_steps[-1]

    if Parameters["Model"] == 1:
        D_true = 1/4*(Parameters["GAMMA1_SHARE"]*1+(1-Parameters["GAMMA1_SHARE"])*2) * Parameters["a"]**2*Parameters["GAMMA"]
        MQV_true_table = [4*D_true*1,4*D_true*n]
        ax.plot([1,n], MQV_true_table, label ="$<[x(t0-t)-x(t0)]²> = (\\Gamma_1 + 2\\Gamma_2) a^2 t  $", color = "royalblue", 
        linestyle = "solid")
    else :
        D_true = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])) * (Parameters['a']-2*Parameters['b'])**2
        MQV_true_table = [4*D_true*1,4*D_true*n]
        D_eff1 = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])) * (Parameters['a']**2-2*Parameters['a']*Parameters['b']+Parameters['b']**2)
        MQV_eff1_table = [4*D_eff1*1,4*D_eff1*n]
        D_eff2 = 1/4*Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])/(1+Parameters["GAMMA1_SHARE"])*Parameters['a']**2
        MQV_eff2_table = [4*D_eff2*1,4*D_eff2*n]
        ax.plot([1,n], MQV_true_table, label ="<[x(t0-t)-x(t0)]²> = Gamma1*Gamma2/Gamma*(a-2b)²t", color = "lightsteelblue", 
        linestyle = "dotted")
        ax.plot([1,n],MQV_eff1_table, label = "<[x(t0-t)-x(t0)]²> = Gamma1*Gamma2/Gamma*(a²+b²-2ab)t", color = 'cornflowerblue', linestyle = "dotted")
        ax.plot([1,n],MQV_eff2_table, label = "<[x(t0-t)-x(t0)]²> = Gamma1*Gamma2/(2Gamma1+Gamma2)*a²t", color = 'royalblue')


    ax.legend()
    ax.grid()
    ax.set_xlabel("steps (or time steps kt = t)")
    ax.set_ylabel("<[x(t0-t)-x(t0)]²>")
    ax.set_title("Diffusion coefficient D, with respect to time on a {:,d} steps trajectory".format(Parameters["steps"]))
    if Parameters["custom load"]:
        fig.savefig(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}")
    else :
        fig.savefig(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/model{Parameters['Model']}_step_{Parameters['steps']}")
    
    plt.show()
    
        
        

def Diffusion_onesim(Parameters : dict) -> None :
    #load traj
    trajectory_vector = savings.loadfromfile(Parameters,'traj')
    if Parameters["Model"] == 1:
        D_true = 1/4*(Parameters["GAMMA1_SHARE"]*1+(1-Parameters["GAMMA1_SHARE"])*2) 
    else :
        D_true = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])) * (Parameters['a']-2*Parameters['b'])**2
        
    #O(n²)
    #We only care about the first percents of the trajectory
    n = trajectory_vector.shape[0]*0.02
    if not Parameters["load"]:
        if Parameters["custom load"]:
            MQV_compute= np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_mqv.{Parameters['saving type']}")[0]
            taken_steps = np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_mqv.{Parameters['saving type']}")[1]
        else:
            MQV_compute= np.load("GAMMA1_SHARE_{}/model{}_step_{}_mqv.npy".format(Parameters["GAMMA1_SHARE"],Parameters['Model'], Parameters["steps"]))[0]
            taken_steps = np.load("GAMMA1_SHARE_{}/model{}_step_{}_mqv.npy".format(Parameters["GAMMA1_SHARE"],Parameters['Model'], Parameters["steps"]))[1]
    else :
        #taken_steps = np.linspace(100, n+1, 20, dtype = int)
        taken_steps = np.linspace(n/20,n,20, dtype = int)
        MQV_compute = np.array([MQV(trajectory_vector, k) for k in taken_steps])
        savings.save2file(Parameters,np.stack((MQV_compute,taken_steps), axis = 0),"mqv")
           #to print we multiply 4Dt where t is adimensional so : t = step_number
    n = taken_steps[-1]
    MQV_true_table = [4*D_true*1,4*D_true*n]
    D_eff1 = 1/4*(Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])) * (Parameters['a']**2-2*Parameters['a']*Parameters['b']+Parameters['b']**2)
    MQV_eff1_table = [4*D_eff1*1,4*D_eff1*n]
    D_eff2 = 1/4*Parameters["GAMMA1_SHARE"]*(1-Parameters["GAMMA1_SHARE"])/(1+Parameters["GAMMA1_SHARE"])*Parameters['a']**2
    MQV_eff2_table = [4*D_eff2*1,4*D_eff2*n]


            
    
    fig, ax = plt.subplots(figsize = (16,9))
    ax.set_xlim(1,n)
    ax.plot([1,n], MQV_true_table, label ="<[x(t0-t)-x(t0)]²> = Gamma1*Gamma2/Gamma*(a-2b)²t", color = "lightsteelblue", 
            linestyle = "dotted")
    #
    ax.plot(taken_steps,MQV_compute, label = "Computed <[x(t0-t)-x(t0)]²> value", color = 'red', 
            linestyle = "dashed", marker = "^")
    ax.plot([1,n],MQV_eff1_table, label = "<[x(t0-t)-x(t0)]²> = Gamma1*Gamma2/Gamma*(a²+b²-2ab)t", color = 'cornflowerblue', linestyle = "dotted")
    ax.plot([1,n],MQV_eff2_table, label = "<[x(t0-t)-x(t0)]²> = Gamma1*Gamma2/(2Gamma1+Gamma2)*a²t", color = 'royalblue')

    #
    ax.legend()
    ax.set_xlabel("steps (or time steps kt = t) ")
    ax.set_ylabel("<[x(t0-t)-x(t0)]²>")
    ax.set_title("Diffusion coefficient D, with respect to time on a {} steps trajectory".format(Parameters["steps"]))
    if Parameters["custom load"]:
        plt.savefig(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}")
    else :
        plt.savefig(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/model{Parameters['Model']}_step_{Parameters['steps']}")
    

def Diffusion_gamma(GAMMA_TABLE, D, Parameters) -> None :
    fig, ax = plt.subplots(figsize = (16,9))

    if Parameters["Model"] == 1 :
        D_true = np.array([0.25*(gamma+2*(1-gamma))*Parameters['a']**2 for gamma in GAMMA_TABLE])
        ax.plot(GAMMA_TABLE*Parameters["GAMMA"], D_true, label = 'true')
    else :
        D_one = np.array([Parameters["GAMMA"]*1/4*gamma*(1-gamma)*(Parameters['a']-2*Parameters["b"])**2 for gamma in GAMMA_TABLE])
        D_two = np.array([Parameters["GAMMA"]*1/4*gamma*(1-gamma)*(Parameters['a']**2-2*Parameters['a']*Parameters['b']+Parameters['b'])**2 for gamma in GAMMA_TABLE])
        D_three = np.array([Parameters["GAMMA"]*1/4*gamma*(1-gamma)/(1+gamma)*(Parameters['a'])**2 for gamma in GAMMA_TABLE])
        ax.plot(GAMMA_TABLE*Parameters["GAMMA"], D_one, label = '$D = 1/4 \\ \\frac{\Gamma_1\\Gamma_2}{\\Gamma} (a-2b)^2 $', color = "lightsteelblue", linestyle= "dotted") 
        ax.plot(GAMMA_TABLE*Parameters["GAMMA"], D_two, label = '$D = 1/4 \\ \\frac{\\Gamma_1\\Gamma_2}{\\Gamma} (a^2+b^2-2ab)$', color = "cornflowerblue", linestyle = 'dotted')
        ax.plot(GAMMA_TABLE*Parameters["GAMMA"], D_three, label = '$D = 1/4 \\  \\frac{\\Gamma_1\\Gamma_2}{2\\Gamma_1+\\Gamma_2}a^2$', color= "royalblue")

    axup = ax.twiny()
    ax.set_xlim(0,Parameters["GAMMA"])
    axup.set_xlim(Parameters["GAMMA"],0)
    ax.grid()
    ax.set_xticks(GAMMA_TABLE*Parameters["GAMMA"])
    axup.set_xlabel("$\\Gamma_2$", fontsize=16)

    axup.set_xticks(Parameters["GAMMA"]*(1-GAMMA_TABLE))
    ax.plot(GAMMA_TABLE*Parameters["GAMMA"], D*Parameters["GAMMA"], label = 'computed', color='red', linestyle='dotted', marker='o')
    ax.set_xlabel("$\\Gamma_1$", fontsize=16)
    ax.set_ylabel("D", fontsize = 16)
    ax.set_title("Diffusion coefficient D, with respect to gamma frequencies, on a {}M steps trajectory ".format(Parameters["steps"]/1000000), fontsize=20)
    ax.text(0.03,0.97,f'''$\\Gamma = {Parameters["GAMMA"]}$''',transform=ax.transAxes, fontsize = 15, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.legend(fontsize = 15)

    fig.savefig("D_gamma/figure_D")

def choose_color_computed(nb:int) -> list[str] :
    if nb <= len(COMPUTED_COLOR) :
        return COMPUTED_COLOR
    else :
        return mcolors.CSS4_COLORS.keys()