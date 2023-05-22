import numpy as np
import math
import print_settings 
from path_generator import *

LAYER =50
def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,100)
        rad = 10
        x = rad*np.cos(arg)
        y = rad*np.sin(arg)
        z = np.full_like(arg, height*print_settings.layer_height+0.2)
        wall, wall_2 = Path(x, y, z), Path(x, y, z)
        wall = Transform.move(wall, pitch = np.pi/2)
        wall = Transform.move(wall, x = 10)
        
        wall_2  =Transform.move(wall_2, x = 10)
        wall_2 = Transform.move(wall, pitch = np.pi/2)
        full_object.append(wall)
        full_object.append(wall_2)
        
            



        

    return full_object

