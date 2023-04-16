import numpy as np
import math
from path_generator import *

LAYER=2



def object_modeling():
    full_object=[]
    for height in range(LAYER):
        x = np.array([10,-10,-10,10,10], dtype = float)
        y = np.array([10,10,-10,-10,10], dtype = float)
        z = np.full_like(x, height*0.2+0.2)
        layer = Path(x, y, z)
        full_object.append(layer)

    return full_object

