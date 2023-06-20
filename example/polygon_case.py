import numpy as np
import math
from path_generator import *

LAYER=50
N = 6 #polygon number


def object_modeling():
    pos_array=[]
    full_object = []
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,N+1)
        rad = 25
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*0.2+0.2)
        wall = Path(x, y, z)
        full_object.append(wall)
        if height==0:
            bottom = Transform.fill(wall, infill_distance = 0.4, offset = -0.4)
            full_object.append(bottom)


    return full_object

