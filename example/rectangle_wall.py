import numpy as np
import math
from print_functions import *
LAYER=20



def object_modeling():
    full_object=[]
    for height in range(LAYER):
        '''arg = np.linspace(0, np.pi*2,5)
        rad = [10 for arg_i in arg]
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*0.3+0.2)
        F = np.full_like(x, 400)
        E = np.full_like(x,0)
        layer = print_layer(x, y, z,F,E)
        full_object.append(layer)'''
        
        x = np.array([10,-10,-10,10,10],dtype = float)
        y = np.array([10,10,-10,-10,10],dtype = float)
        z = np.full_like(x, height*0.3+0.2)
        layer = print_layer(x, y, z)
        full_object.append(layer)

    return full_object

