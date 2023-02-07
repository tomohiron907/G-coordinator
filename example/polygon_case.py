import numpy as np
import math
from print_functions import *

LAYER=50



def object_modeling():
    pos_array=[]
    full_object = []
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,7)
        rad = 25
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*0.2+0.2)
        wall = print_layer(x, y, z)
        full_object.append(wall)
        if height==0:
            rad=25
            x = (rad-0.4)*np.cos(arg)
            y = (rad-0.4)*np.sin(arg)
            z = np.full_like(arg, height*0.2+0.2)
            layer_pos = np.column_stack([x, y, z])
            infill_pos = line_fill(layer_pos,0.4,0)
            bottom = print_layer(infill_pos[0], infill_pos[1], infill_pos[2])
            full_object.append(bottom)
            



        
        

    return full_object

