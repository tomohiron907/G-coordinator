import numpy as np
import math
import print_settings 
from path_generator import *
from infill_generator import *

LAYER =75
nozzle = print

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(np.pi/4, np.pi/4+np.pi*2,5)
        rad = 70 
        x = rad*np.cos(arg)*1.618
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*print_settings.layer_height+0.2)
        wall = Path(x, y, z)
        inner_wall = Transform.offset(wall, -0.7)
        infill = gyroid_infill(wall,infill_distance = 8)
        wall.z_hop = False
        wall.retraction = False
        full_object.append(wall)
        full_object.append(inner_wall)
        full_object.append(infill)
            



        

    return full_object

