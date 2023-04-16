import numpy as np
import math
from path_generator import *
'''
NOZZLE = 0.4
layer_heoght = 0.2
'''
LAYER = 400

def rotation_calc(height):
    rad = np.sqrt(50**2 - (height * 0.2-35)**2)
    return height*0.004

def print_polar(arg, rad, height):
    rotation = rotation_calc(height)
    x = rad*np.cos(arg + rotation)
    y = rad*np.sin(arg + rotation)
    z = np.full_like(arg, height*0.2+0.2)
    layer = Path(x,y,z)
    return layer
    

def object_modeling():
    full_object=[]
    R = 50
    layer_thick = 0.2
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,801)
        rad = np.sqrt(R**2 - (height * layer_thick-35)**2)
        rad += 3 * np.floor(1.05 * abs( np.sin(arg * 50)))
        wall = print_polar(arg, rad, height)
        full_object.append(wall)
        
    for height in range(400, 426):
        arg = np.linspace(0, np.pi*2,401)
        rad = np.sqrt(R**2 - (399 * layer_thick-35)**2)
        top_wall = print_polar(arg, rad, height)
        full_object.append(top_wall)
        full_object.append(Transform.offset(top_wall, -0.4))


        
        

    return full_object

