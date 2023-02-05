import numpy as np
import math
import draw_object

LAYER=10



def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,100)
        rad = [30-0.4 for arg_i in arg]
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*0.2+0.2)
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
            



        
        

    return pos_array

