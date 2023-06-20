import numpy as np
import math
import print_settings 
from path_generator import *
from console import *


LAYER =50

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,100)
        rad = 10
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*print_settings.layer_height+0.2)
        wall = Path(x, y, z)
        full_object.append(wall)
        print(f'wall at height {height}')



    return full_object

