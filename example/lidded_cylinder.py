import numpy as np
import math
from path_generator import *
LAYER=10



def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,100)
        rad = [10 for arg_i in arg]
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*0.4+0.4)
        layer = Path(x,y,z)
        full_object.append(layer)
    
    for polar in range(12):
        arg = np.linspace(0, np.pi*2,100)
        rad = 10-0.76-polar *0.76
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, LAYER*0.4)
        layer = Path(x,y,z)
        full_object.append(layer)



        
        

    return full_object

