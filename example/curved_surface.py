import numpy as np
import math
from path_generator import *
import noise

'''
NOZZLE = 0.4
layer height = 0.2
'''


LAYER=500
a = 3
b = 1/25

def function(i, j):
    i *= a
    j *= b
    value = noise.pnoise2(i, j, octaves=4, persistence=0.2, lacunarity=1.0, repeatx=512, repeaty=512, base=0)
    return value*20

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        t = np.linspace(0,1,400)
        x = t*100-50
        y = np.array([ function(height/LAYER, i) for i in x ])
        z = np.full_like(t, height*0.2+0.2)
        
        wall = Path(x, y, z)
        y -= 6*np.floor( abs(1.05 * np.sin(t * 2 * np.pi * 20))) + 0.4
        wall.z_hop = True
        wall_2 = Path(x, y, z)
        wall_2.z_hop = True
        full_object.append(wall)
        full_object.append(wall_2)
        
        
        
        x = np.array([-50, 50], dtype = float)
        y = np.array([20, 20], dtype = float)
        z = np.full_like(x,height*0.2+0.2)
        back_wall = Path(x, y, z)
        full_object.append(back_wall)
        
        
        for i in range(6):
            x = np.full(2, i*20 -50, dtype = float)
            y = np.array([ 20, function(height/LAYER, i*20 -50) ])
            z = np.full_like(x,height*0.2+0.2)
            connect_wall = Path(x, y, z)
            full_object.append(connect_wall )
        

        
        

        
        
        

        


        
        

    return full_object

