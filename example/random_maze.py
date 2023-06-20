import numpy as np
from path_generator import *
import print_settings
import random

nozzle = print_settings.nozzle_diameter
thickness = print_settings.layer_height

LAYER = 20
s = 10
def line(x_pos, y_pos, a):
    if a:
        x = np.array([x_pos*s, x_pos*s+s], dtype = float)
        y = np.array([y_pos*s, y_pos*s+s], dtype = float)
        return x-100, y-100
    else:
        x = np.array([x_pos*s, x_pos*s+s], dtype = float)
        y = np.array([y_pos*s+s, y_pos*s], dtype = float)
        return x-100, y-100


def object_modeling():
    full_object=[]
    random_slope = [[  bool(random.getrandbits(1))   for j in range(20)] for j in range(20)]
    for height in range(LAYER):
        for i in range(20):
            for j in range(20):
                a = random_slope[i][j]
                x, y = line(i, j, a)
                z = np.full_like(x, (height+1)*thickness+1)
                seg = Path(x, y, z)
                full_object.append(seg)
    return full_object