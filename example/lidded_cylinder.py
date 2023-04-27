import numpy as np
import math
from path_generator import *
import print_settings
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
        offset = Transform.offset(layer, 0)
    for i in range(20):
        offset = Transform.offset(offset, - print_settings.nozzle_diameter)
        full_object.append(offset)
        



        
        

    return full_object

