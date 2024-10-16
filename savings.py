import numpy as np
import matplotlib.pyplot as plt



        
def save2file(Parameters:dict, arraytosave:np.ndarray) -> None :
    print("saving location is {}".format(Parameters["table save path"] + "last_path" + Parameters["saving type"]))
    if Parameters["saving type"] == ".npy" :
        np.save(Parameters["table save path"] + "last_path", arraytosave)
    elif Parameters["saving type"] == ".txt" :
        np.savetxt(Parameters["table save path"] + "last_path", arraytosave)
    else :
        print("NOT IMPLEMENTED EXTENSION")
    
    
    
    
    
    
    
 

