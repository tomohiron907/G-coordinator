

# Please execute this code after changing the machine setting's 
# kinematics to 'bed_rotate_bc'.
# Author: @_gear_geek_'


import numpy as np
import math
import print_settings 
from path_generator import *

LAYER =50

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        rad = 10
        x = [rad, rad]
        y = [0, 0]
        buf_z = height*print_settings.layer_height+0.2
        z = [buf_z, buf_z]
        rot = [math.pi*2*height, math.pi*2*(height+1)]
        wall = Path(x, y, z, rot)
        full_object.append(wall)        

    return full_object

