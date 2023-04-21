import numpy as np
import math
import print_settings 
from path_generator import *

LAYER =20
a = 15
b = 17
d = np.pi/2

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        t = np.linspace(0, np.pi* 1.5,1000)
        rad = 60
        x = rad*np.sin(a*t + d)
        y = rad*np.sin(b*t)
        z = np.full_like(t, height*print_settings.LAYER+0.2)
        wall = Path(x, y, z)
        
        full_object.append(wall)
        


    return full_object
    