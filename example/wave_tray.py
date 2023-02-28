import numpy as np
import math
from print_functions import *


'''
NOZZLE = 1
LAYER = 1
Print_speed = 500
Ext_multiplier = 1
'''

LAYER=40
base_rad = 60




def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,403)
        amp = 2
        rad = base_rad+amp*np.sin(arg*100.5+np.pi*height)
        rad += 7*np.sin((height/LAYER)*np.pi)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.linspace(height*1,(height+1)*1,403)
        wave_wall = print_layer(x, y, z)
        full_object.append(wave_wall)

        if height <2:
            arg = np.linspace(0, np.pi*2,401)
            rad = [base_rad-2  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*1+1)
            #F = np.full_like(arg,500)
            inner_wall = print_layer(x, y, z,Feed = 1000)
            full_object.append(inner_wall)

            
            
            
            
            arg = np.linspace(0, np.pi*2,401)
            rad = [base_rad-2-0.5  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*1+1)

            layer_pos = np.column_stack([x, y, z])
            infill = line_fill(layer_pos,2.5,np.pi/4*(-1)**height)
            bottom = print_layer(infill[0], infill[1], infill[2],Feed = 1000)
            full_object.append(bottom)
            
            x = 0
            y = 0
            z = 10
            
            travel_point = print_layer(x, y, z)
            full_object.append(travel_point)


        
        

    return full_object

