import numpy as np
import math
from path_generator import *
from infill_generator import *

LAYER=80
nozzle = print_settings.nozzle_diameter
thickness = print_settings.layer_height
a = 4
L = 40


def quarter_func(arg):
    rad = L * (np.cos(arg)**a + np.sin(arg)**a)**(-1/a)
    return rad

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        t = np.linspace(0, 2*np.pi, 200)
        rad = quarter_func(t)
        x = rad * np.cos(t)
        y = rad * np.sin(t)
        z = np.full_like(x, thickness * (height +1))
        wall = Path(x, y, z)
        full_object.append(wall)
        outer_wall = Transform.offset(wall, 0.4)
        full_object.append(outer_wall)
        
        if height<50:
            gyroid = gyroid_infill(wall, infill_distance = 2)
            full_object.append(gyroid)
        
       
        


    return full_object

