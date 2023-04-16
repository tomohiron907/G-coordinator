import numpy as np
import math
from path_generator import *

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
        rad = 40-30*1.5*(height/LAYER)+30*1.5*(height/LAYER)**2+amp*np.floor(abs(1.2*np.sin(arg*25))) 
        angle = rotation(height)
        x = rad*np.cos(arg+angle)
        y = rad*np.sin(arg+angle)
        z = np.full_like(arg, height*0.3+0.2)
        outer_wall = Path(x, y, z)
        full_object.append(outer_wall)
        

        for i in range(2):
            arg = np.linspace(0, np.pi*2,201)
            rad = 40-30*1.5*(height/LAYER)+30*1.5*(height/LAYER)**2 - 0.4*(i+1) 
            angle = rotation(height)
            x = rad*np.cos(arg+angle)
            y = rad*np.sin(arg+angle)
            z = np.full_like(arg, height*0.3+0.2)
            inner_wall = Path(x, y, z)
            full_object.append(inner_wall)
        


    return full_object
    

