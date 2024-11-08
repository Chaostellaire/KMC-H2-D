import numpy as np
import matplotlib.pyplot as plt
import os


        
def save2file(Parameters:dict, arraytosave:np.ndarray, arraytype:str) -> None :
    directory_path = f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}"
    os.makedirs(directory_path, exist_ok=True)
    print(f"saving location is {directory_path}")
    if Parameters['custom save'] :
        if Parameters["saving type"] == "npy" :
            np.save(f"{directory_path}/{Parameters['load path']}_T{Parameters['current trajectory']}{arraytype}.{Parameters['saving type']}", arraytosave)
        elif Parameters["saving type"] == "txt" :
            np.savetxt(f"{directory_path}/{Parameters['load path']}_T{Parameters['current trajectory']}{arraytype}.{Parameters['saving type']}", arraytosave)
        else :
            print("NOT IMPLEMENTED EXTENSION")
    
    else :   
        if Parameters["saving type"] == "npy" :
            np.save(f"{directory_path}/model{Parameters['Model']}_step_{Parameters['steps']}_T{Parameters['current trajectory']}{arraytype}.{Parameters['saving type']}", arraytosave)
        elif Parameters["saving type"] == "txt" :
            np.savetxt(f"{directory_path}/model{Parameters['Model']}_step_{Parameters['steps']}_T{Parameters['current trajectory']}{arraytype}.{Parameters['saving type']}", arraytosave)
        else :
            print("NOT IMPLEMENTED EXTENSION")

def loadtraj(Parameters:dict) -> np.ndarray :
    if Parameters["custom load"]:
        L = np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_T{Parameters['current trajectory']}traj.{Parameters['saving type']}")
    else:
        L = np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/model{Parameters['Model']}_step_{Parameters['steps']}_T{Parameters['current trajectory']}traj.{Parameters['saving type']}")
    return L

def loadmqv(Parameters:dict) -> np.ndarray :
    if Parameters["custom load"]:
        return np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/{Parameters['load path']}_T{Parameters['current trajectory']}mqv.{Parameters['saving type']}")
    else:
        return np.load(f"GAMMA1_SHARE_{Parameters['GAMMA1_SHARE']}/model{Parameters['Model']}_step_{Parameters['steps']}_T{Parameters['current trajectory']}mqv.{Parameters['saving type']}")

    
    
    
 

