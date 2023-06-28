import math
import numpy as np
import print_settings 
from path_generator import *
from infill_generator import *
from console import *

LAYER = 100

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, 2*np.pi, 100)
        x = 10 * np.cos(arg)
        y = 10 * np.sin(arg)
        z = np.full_like(arg, (height+1) * print_settings.layer_height)
        wall = Path(x, y, z)
        full_object.append(wall)
        print(f'layer at {height=}')
        
    return full_object