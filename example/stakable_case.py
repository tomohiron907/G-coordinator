import numpy as np
import math
from path_generator import *

LAYER=100
THICK = 0.7
a = 2

def quarter_func(arg):
    rad = 40 * (np.cos(arg)**a + np.sin(arg)**a)**(-1/a)
    return rad

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        t = np.linspace(0, 2*np.pi, 200)
        r = 30
        x = r * np.power(np.cos(t), 1/a)
        y = r * np.power(np.sin(t), 1/a)
        z = np.full_like(x, 0.2 * (height +1))
        wall = Path(x, y, z)
        full_object.append(wall)
        


    return full_object

