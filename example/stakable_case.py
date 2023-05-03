import numpy as np
import math
from path_generator import *

LAYER=120
nozzle = print_settings.nozzle_diameter
thickness = print_settings.layer_height
a = 4
depth = 35


def quarter_func(arg):
    rad = 40 * (np.cos(arg)**a + np.sin(arg)**a)**(-1/a)
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
        
        if height>depth:
            wall = Transform.offset(wall, nozzle*4)
        full_object.append(wall)
        
        for i in range(2):
            inner_wall = Transform.offset(wall, -nozzle*(i+1))
            full_object.append(inner_wall)
            
        if height == depth or height == depth-1:
            offset = wall
            for i in range(4):
                offset = Transform.offset(offset, nozzle)
                full_object.append(offset)
                
        if height <2:
            infill_wall = Transform.offset(inner_wall, -nozzle)
            infill_wall.z_hop = True
            infill_wall.retraction = True
            bottom  = Transform.fill(infill_wall, offset = -nozzle*0.75, infill_distance = 2*nozzle)
            bottom = Transform.rotate(bottom, np.pi/2*height)
            bottom.z_hop = True
            bottom.retraction = True
            full_object.append(infill_wall)
            full_object.append(bottom)
        


    return full_object

