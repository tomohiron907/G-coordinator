import numpy as np
import math
from path_generator import *
from infill_generator import *


LAYER=56
nozzle = print_settings.nozzle_diameter
thickness = print_settings.layer_height
a = 4
depth = 35



def quarter_func(arg, L):
    rad = L * (np.cos(arg)**a + np.sin(arg)**a)**(-1/a)
    return rad


def object_modeling():
    full_object=[]
    for height in range(LAYER):
        t = np.linspace(0, 2*np.pi, 200)
        rad = quarter_func(t, 40)
        x = rad * np.cos(t)
        y = rad * np.sin(t)
        z = np.full_like(x, thickness * (height +1))
        wall = Path(x, y, z)
        full_object.append(wall)
        outer_wall = Transform.offset(wall, 0.4)
        full_object.append(outer_wall)
        
        if height<6:
            x = 4.4 * np.cos(t)
            y = 4.4 * np.sin(t)
            z = np.full_like(x, thickness * (height +1))
            hole = Path(x, y, z)
            full_object.append(hole)
            inner_hole = Transform.offset(hole, -0.4)
            full_object.append(inner_hole)
            
            contour = PathList([wall, hole])
            infill = line_infill(contour, density = 0.98, angle = np.pi/4 + np.pi/2*height)
            infill.z_hop = True
            infill.retraction = True
            full_object.append(infill)
        elif height>=6 and height<57:
            
            t = np.linspace(0, 2*np.pi, 1000)
            L = 30 - 1.2-0.4+np.sqrt(10**2 - (height*0.2-10)**2)
            rad = quarter_func(t, L)
            if height<11:
                rad -= 2*np.floor(1.003*abs(np.cos(t*6)))
            x = rad * np.cos(t)
            y = rad * np.sin(t)
            z = np.full_like(x, thickness * (height +1))
            scale = Path(x, y, z)
            full_object.append(scale)
            
            
            t = np.linspace(0, 2*np.pi, 200)
            L = 30 - 1.2+np.sqrt(10**2 - (height*0.2-10)**2)
            rad = quarter_func(t, L)
            x = rad * np.cos(t)
            y = rad * np.sin(t)
            z = np.full_like(x, thickness * (height +1))
            wall = Path(x, y, z)
            full_object.append(wall)
            outer_wall = Transform.offset(wall, 0.4)
            full_object.append(outer_wall)
            outer_wall = Transform.offset(outer_wall, 0.4)
            full_object.append(outer_wall)
            
            
    
        
       
        



    return full_object


