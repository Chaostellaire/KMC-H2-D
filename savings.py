import numpy as np
import matplotlib.pyplot as plt
import os


        
def save2file(Parameters:dict, arraytosave:np.ndarray) -> None :
    directory_path = f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}"
    os.makedirs(directory_path, exist_ok=True)
    print(f"saving location is {directory_path}")
    if Parameters["saving type"] == "npy" :
        np.save(f"{directory_path}/step_{Parameters['steps']}.{Parameters['saving type']}", arraytosave)
    elif Parameters["saving type"] == "txt" :
        np.savetxt(f"{directory_path}/step_{Parameters['steps']}.{Parameters['saving type']}", arraytosave)
    else :
        print("NOT IMPLEMENTED EXTENSION")
    
    
    
    
    
    
    
 

