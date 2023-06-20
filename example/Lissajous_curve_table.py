import numpy as np
import math
import print_settings 
from path_generator import *

LAYER =20
#ext_multiplier = 1.4

def lissajous(a, b, d, height):
    t = np.linspace(0, np.pi* 2,400)
    rad = 16
    gcd = math.gcd(a, b)
    if gcd >1:
        a_2=a/gcd
        b_2=b/gcd
    else:
        a_2 = a
        b_2 = b
    x = rad*np.sin(a_2*t + d)+a*40-20-100
    y = rad*np.sin(b_2*t)+b*40-20-100
    z = np.full_like(t, (height+1)*print_settings.layer_height)
    
    wall = Path(x, y, z)
    if height == 0:
        wall.z_hop = True
    return wall

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        for i in range(0, 5):
            for j in range(0, 5):
                curve = lissajous(i+1, j+1, np.pi/2.86*(i+1)*(j+1), height)
                full_object.append(curve)


    return full_object
