import numpy as np
import math
import draw_object
import print_functions
LAYER=30

def rotation_calc(height):
    t = 2*np.pi/100/2
    rotation = t*(-1)** height/2
    return rotation



def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,401)
        amp = 2
        rad = [75+amp*math.sin(arg_i*100)-height/1.2  for arg_i in arg]
        rotation = rotation_calc(height)
        x = rad*np.cos(arg + rotation)
        y = rad*np.sin(arg + rotation)
        z = np.full_like(arg, height*0.7+0.7)

        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        


        
        

    return pos_array

