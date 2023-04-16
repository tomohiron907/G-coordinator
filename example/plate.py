import numpy as np
from path_generator import *

LAYER = 2
def object_modeling():
    full_object=[]
    for height in range(LAYER):
        x = np.array([100,-100,-100,100,100], dtype = float)
        y = np.array([100,100,-100,-100,100], dtype = float)
        z = np.full_like(x, height*0.2+0.2)
        wall = Path(x, y, z)
        full_object.append(wall)
        infill = Transform.fill(wall, offset = -0.8, infill_distance = 0.8, angle = np.pi/4 + np.pi/2 *height)
        full_object.append(infill)

    return full_object