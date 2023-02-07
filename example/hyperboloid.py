import numpy as np
import math
from print_functions import *

LAYER=250

def rotation(height):
    t = height / LAYER 
    angle = math.atan(t/(1-t))
    return angle


def amp_calc(height):
    if height > LAYER *  0.94:
        amp = 4 * math.cos((height-0.94 * LAYER)/ (0.06 * LAYER) * np.pi / 2)
    elif height < LAYER * 0.06 :
        amp = 4 * math.sin((height)/ (0.06 * LAYER) * np.pi / 2)
        
    else :
        amp = 4
    return amp


def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,401)
        amp = amp_calc(height)
        rad = [40-30*1.5*(height/LAYER)+30*1.5*(height/LAYER)**2+amp*math.floor(abs(1.2*math.sin(arg_i*25))) for arg_i in arg]

        angle = rotation(height)
        x = rad*np.cos(arg+angle)
        y = rad*np.sin(arg+angle)
        z = np.full_like(arg, height*0.3+0.2)
        layer_pos = np.column_stack([x, y, z])
        outer_wall = print_layer(x, y, z)
        full_object.append(outer_wall)
        
        
        
        
        
        
        
        for i in range(2):
            arg = np.linspace(0, np.pi*2,201)
            rad = [40-30*1.5*(height/LAYER)+30*1.5*(height/LAYER)**2 - 0.6  for arg_i in arg]
            rad = [ rad_i-0.6*i for rad_i in rad]
            angle = rotation(height)
            x = rad*np.cos(arg+angle)
            y = rad*np.sin(arg+angle)
            z = np.full_like(arg, height*0.3+0.2)
            inner_wall = print_layer(x, y, z)
            full_object.append(inner_wall)
        



        
        

    return full_object
    

