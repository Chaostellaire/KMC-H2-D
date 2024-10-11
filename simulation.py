import numpy as np;
import kinmontecarlo as KMC

class Simulation :
    GAMMA : float = 1;

    def __init__(self, steps:int, GAMMA1_SHARE : float) :
        """
        steps : number of steps in a given sim, used to generate arrays
        
        *******************

        ~~Creates attributes~~ :
        H_path : stores the simulation result
        H_choices : stores if we took the <1 0> direction (coded by 1) or <1 1> direction (coded by 2)
        steps : becomes an attribute 
        GAMMAi_SHARE : i can be either 1 or 2, gives dimensionless GAMMA1 or GAMMA2

        """
        self.H_path = np.empty((steps+1, 2), dtype = int)
        self.H_choices = np.zeros((steps,), dtype = int)
        self.steps = steps
        self.GAMMA1 = GAMMA1_SHARE
        self.GAMMA2 = 1-GAMMA1_SHARE
    
    def run(self) :
        self.H_path, self.H_choices = KMC.trajectory(self.steps, self.GAMMA1)
    
