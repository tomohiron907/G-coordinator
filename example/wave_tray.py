import numpy as np
import math
from path_generator import *

'''
NOZZLE = 1
LAYER = 1
Print_speed = 500
Ext_multiplier = 1.4
'''

LAYER=40
base_rad = 60


def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,403)
        amp = 2
        z = np.linspace(height*1,(height+1)*1,403)
        rad = base_rad
        rad += 7*np.sin((z/LAYER)*np.pi)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        circle = Path(x, y, z)
        
        
        rad+=amp*np.sin(arg*100.5+np.pi*height)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        wave_wall = Path(x, y, z)
        full_object.append(wave_wall)
        
        if height<2:
            inner_wall = Transform.offset(circle, -2)
            full_object.append(inner_wall)
            bottom = Transform.fill(inner_wall, 2, offset = -0.8)
            full_object.append(Transform.rotate(bottom, np.pi/2*height))
            


    return full_object

