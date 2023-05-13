import numpy as np
import math
import print_settings 
from path_generator import *

LAYER =50
nozzle = print
print('hoge')
def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,100)
        rad = 10
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*print_settings.layer_height+0.2)
        rot = arg
        tilt = [np.pi/2/100*height]*len(x)
        wall = Path(x, y, z, rot, tilt)
        full_object.append(wall)



        

    return full_object

