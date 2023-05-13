import numpy as np
import math
import print_settings 
from path_generator import *

LAYER =50
nozzle = print
print('hoge')
def object_modeling():
    full_object=[]
    radius = 50
    cnt = 0
    while radius < 55:
        angle = np.linspace(0, np.pi,180)
        if cnt%2==0:
            x = radius * np.cos(angle)
        else:
            x = -radius * np.cos(angle)
        y = [0] * len(x)
        z = radius * np.sin(angle)
        rot = [math.pi / 2.0] * len(x)
        tilt = [math.pi / 4.0] * len(x)
        wall = Path(x, y, z, rot, tilt)
        wall.extrusion_multiplier = 10.0
        full_object.append(wall)
        radius += 0.6
        cnt += 1

    return full_object