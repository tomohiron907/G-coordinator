import numpy as np
import math
from path_generator import *


'''
NOZZLE = 1
LAYER = 1
Print_speed = 500
Ext_multiplier = 1
'''

LAYER=110
base_rad = 35


def wave(x):
    y = np.arccos(np.cos(x + np.pi/2))/np.pi * 2 -1
    return y

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,203)
        amp = 3
        z = np.linspace(height*1,(height+1)*1,203)
        rad = base_rad
        off_rad = 8
        
        if height < LAYER* 0.175:
            rad += 0
            rad += off_rad*np.sin((z/LAYER) * 5*np.pi/2)
        else:
            rad += amp*np.sin(arg*50.5+height*np.pi)+off_rad
            #rad += 4*np.sin((z/LAYER - 0.1) * 5*np.pi/2*3)
            b = 6 * np.sin((z / LAYER-0.175) * np.pi * 3.5  )
            a = 3
            rad += b * np.sin(a * arg)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        wave_wall = Path(x, y, z)
        full_object.append(wave_wall)
        


        if height <2:
            arg = np.linspace(0, np.pi*2,401)
            rad = [base_rad-0.7  for arg_i in arg]
            #rotation = rotation_calc(height)
            z = np.full_like(arg, height*1+1)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            
            inner_wall = Path(x, y, z)
            full_object.append(inner_wall)
            bottom = Transform.fill(inner_wall, infill_distance = 1, offset = 0.4, angle = np.pi/4+ np.pi/2 * height)
            full_object.append(bottom)


    return full_object

