import numpy as np
import math
from print_functions import *
import parameter_curve_func as pf

'''
NOZZLE = 0.8
LAYER = 0.4
Print_speed = 700
Ext_multiplier = 2.6
'''

LAYER=100
base_rad = 50




def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,203)
        amp = 2
        rad = base_rad+amp*np.sin(arg*50.5+np.pi*height) 
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.linspace(height*0.7,(height+1)*0.7,203)
        wave_wall = print_layer(x, y, z)
        full_object.append(wave_wall)

        if height <2:
            arg = np.linspace(0, np.pi*2,401)
            rad = [base_rad-2  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)
            #F = np.full_like(arg,500)
            inner_wall = print_layer(x, y, z)
            full_object.append(inner_wall)

            
            
            
            
            arg = np.linspace(0, np.pi*2,401)
            rad = [base_rad-2-1  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)

            layer_pos = np.column_stack([x, y, z])
            infill = line_fill(layer_pos,1.6,np.pi/4*(-1)**height)
            bottom = print_layer(infill[0], infill[1], infill[2])
            full_object.append(bottom)


        
        

    return full_object

