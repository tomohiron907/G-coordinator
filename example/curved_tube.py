import numpy as np
import math
import print_settings 
from path_generator import *

LAYER =200
nozzle = print_settings.nozzle_diameter

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, 2 * np.pi , 100)
        rad = 10
        x = rad * np.cos(arg)
        y = rad * np.sin(arg)
        z = np.full_like(x, 0)
        circle = Path(x, y, z)

        circle = Transform.move(circle, pitch = -np.pi/2*height/LAYER)
        #circle = Transform.move(circle, z = height*0.2, x = height*0.2)
        circle = Transform.move(circle, x = 50-50*np.cos(np.pi/2*height/LAYER))
        full_object.append(circle)
        
    
    return full_object

