import numpy as np
import math
from path_generator import *

LAYER=380
def rotation_calc(height):
    x=height/LAYER
    rotation=math.sin((x)*2.5*np.pi)
    return rotation*0.3

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg=np.linspace(0,2*np.pi,481)
        rad=22+ 4*np.floor(1.05*abs(np.sin(arg*40))) 
        if height/LAYER<=0.25:
            rad=rad-5*(1-np.sin((height/LAYER)/0.25*np.pi/2))
        rotation = rotation_calc(height)

        x = rad*np.cos(arg+rotation)
        y = rad*np.sin(arg+rotation)
        z = np.full_like(arg, height*0.2+0.2)
        wall = Path(x, y, z)
        full_object.append(wall)

        


        # _c means inner wall
        arg_c=np.linspace(0,-2*np.pi,201)
        rad_c=22-0.25 
        if height/LAYER<=0.25:
            rad_c = rad_c-5*(1-np.sin((height/LAYER)/0.25*np.pi/2)) 
        rotation = rotation_calc(height)
        x_c = rad_c*np.cos(arg_c+rotation)
        y_c = rad_c*np.sin(arg_c+rotation)
        z_c = np.full_like(arg_c, height*0.2+0.2)
        wall_c = Path(x_c, y_c, z_c)
        full_object.append(wall_c)
        

    return full_object