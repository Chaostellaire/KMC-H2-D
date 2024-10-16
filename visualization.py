import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_simulation(L, Parameters):
        if Parameters['visu']:
            # Create the figure and axis
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
                atom.set_data(x, y)
                return atom,

            # Initialize writer for saving the video
            writervideo = animation.FFMpegWriter(fps=Parameters['fps'])  # Ensure ffmpeg is installed

            # Create the animation
            ani = animation.FuncAnimation(fig, animate, frames=len(L), init_func=init, blit=True)
            
            # Save the animation
            ani.save(f"anim_steps{Parameters['steps']}_fps{Parameters['fps']}.mp4", writer=writervideo)

        
