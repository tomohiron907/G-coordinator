import numpy as np
import math
import print_setting
from path_generator import *

LAYER=50



def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,100)
        rad = 10
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*print_setting.LAYER+0.2)
        wall = Path(x, y, z)
        inner_wall = Transform.offset(wall, 0.4)
        full_object.append(wall)
        full_object.append(inner_wall)
        
        if height <2 :
            bottom = Transform.fill(wall, infill_distance = print_setting.NOZZLE, offset = -print_setting.NOZZLE)
            bottom = Transform.rotate(bottom, np.pi/2*height)
            full_object.append(bottom)
            



        
        

    return full_object

