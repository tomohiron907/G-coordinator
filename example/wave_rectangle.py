import numpy as np
import math
import print_functions
from print_functions import print_layer
import parameter_curve_func as pf

'''
NOZZLE = 0.8
LAYER = 0.4
Print_speed = 700
Ext_multiplier = 2.6
'''

LAYER=50

def rotation_calc(height):
    t = 2*np.pi/50/2
    rotation = t*(-1)** height/2
    return rotation



def object_modeling():
    pos_array=[]
    full_object = []
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,203)
        amp = 2
        rad = 30+amp*np.sin(arg*50.5+np.pi*height) 
        rotation = rotation_calc(height)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.linspace(height*0.7,(height+1)*0.7,203)
        curve = print_layer(x,y,z)
        full_object.append(curve)

        


        
        

    return full_object
    

