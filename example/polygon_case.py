import numpy as np
import math
import print_functions

LAYER=50



def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,7)
        rad = [25 for arg_i in arg]
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*0.2+0.2)
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        if height==0:
            rad=25
            x = (rad-0.4)*np.cos(arg)
            y = (rad-0.4)*np.sin(arg)
            z = np.full_like(arg, height*0.2+0.2)
            layer_pos = np.column_stack([x, y, z])
            infill_pos = print_functions.line_fill(layer_pos)
            pos_array.append(infill_pos)
            



        
        

    return pos_array

