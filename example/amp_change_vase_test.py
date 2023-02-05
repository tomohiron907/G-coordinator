import numpy as np
import math
import draw_object
import print_functions
LAYER=150

def rotation_calc(height):
    t = 2*np.pi/40/2
    rotation = t*(-1)** height/2
    return rotation


def amp_calc(height):
    if height/LAYER<0.4:
        amp = height/LAYER/0.4
    elif height/LAYER>=0.4 and height/LAYER<0.9:
        amp = (0.9-height/LAYER) / 0.5
    else:
        amp = 0
    return amp*1.3

def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,161)
        if height/LAYER>0.9:
            rad = [ 17 for arg_i in arg]
        else:
            amp = amp_calc(height)
            rad = [27+amp*math.sin(arg_i*40) - 10*math.cos(height/LAYER/0.9*np.pi*2) for arg_i in arg]
        rotation = rotation_calc(height)
        x = rad*np.cos(arg + rotation)
        y = rad*np.sin(arg + rotation)
        z = np.full_like(arg, height*0.7+0.7)

        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        if height<3:
            rad = [ 17-1 for arg_i in arg]
            x = (rad)*np.cos(arg )
            y = (rad)*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)

            layer_pos = np.column_stack([x, y, z])
            fill_pos = print_functions.line_fill(layer_pos,0.4)
            pos_array.append(fill_pos)


        
        

    return pos_array

