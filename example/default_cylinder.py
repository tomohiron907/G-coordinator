import numpy as np
import math

from print_functions import *
LAYER=10



def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,100)
        rad = 10
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*0.2+0.2)
        layer = print_layer(x,y,z)
        full_object.append(layer)
            



        
        

    return full_object

