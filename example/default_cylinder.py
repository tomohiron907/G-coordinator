import numpy as np
import math
import draw_object
import print_functions

LAYER=150

def rotation_calc(height):
    t = 2*np.pi/40/2*0.8
    rotation = t* height
    return rotation*0.03

def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,4)
        rad = [30 for arg_i in arg]
        rotation = rotation_calc(height)
        x = rad*np.cos(arg + rotation)
        y = rad*np.sin(arg + rotation)
        z = np.full_like(arg, height*0.7+0.7)
        #z = [height*0.8+0.8*abs(math.sin(arg_i*40*2*np.pi)) for arg_i in arg]
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        offset = print_functions.contour_offset(layer_pos)
        pos_array.append(offset)

            



        
        

    return pos_array

