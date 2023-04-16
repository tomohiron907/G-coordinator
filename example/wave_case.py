import numpy as np
import math
from path_generator import *


'''
NOZZLE = 1
LAYER = 1
Print_speed = 500
Ext_multiplier = 1
'''

LAYER=90
base_rad = 35




def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,143)
        amp = 3
        z = np.linspace(height*1,(height+1)*1,143)
        rad = base_rad+amp*np.sin(arg*35.5+height*np.pi)
        x = rad*np.cos(arg )+7*np.sin(z/LAYER*2*np.pi*3.2)
        y = rad*np.sin(arg )
        wave_wall = Path(x, y, z)
        full_object.append(wave_wall)

        if height <2:
            arg = np.linspace(0, np.pi*2,401)
            rad = base_rad-3
            z = np.full_like(arg, height*1+1)
            x = rad*np.cos(arg )+7*np.sin(z/LAYER*2*np.pi*3.2)
            y = rad*np.sin(arg )
            inner_wall = Path(x, y, z)
            full_object.append(inner_wall)
            
            bottom = Transform.fill(inner_wall, offset = 0.4, infill_distance = 1, angle = np.pi/4 + np.pi/4 * height)
            full_object.append(bottom)


        
        

    return full_object

