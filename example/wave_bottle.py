import numpy as np
import math
from print_functions import *


'''
NOZZLE = 1
LAYER = 1
Print_speed = 500
Ext_multiplier = 1
'''

LAYER=50
base_rad = 35




def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,201)
        amp = 3
        #z = np.linspace(height*1,(height+1)*1,201)
        rad = base_rad+amp*np.sin(arg*50+height*np.pi)
        rad += 4*np.sin((height/LAYER)*np.pi)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.full_like(arg,height*1 +1)
        wave_wall = print_layer(x, y, z)
        full_object.append(wave_wall)
        
        
        
        arg = np.linspace(0, -np.pi*2,201)
        amp = 3
        rad = base_rad+1.5
        #rad += 7*np.sin((z/LAYER)*np.pi*4.5)
        #rad -= 7*np.cos((z/LAYER)*np.pi*1)-7
        rad += 4*np.sin((height/LAYER)*np.pi)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.full_like(arg,height*1 +1.5)
        wave_wall = print_layer(x, y, z)
        full_object.append(wave_wall)

        if height <2:
            arg = np.linspace(0, np.pi*2,401)
            rad = [base_rad-3  for arg_i in arg]
            #rotation = rotation_calc(height)
            z = np.full_like(arg, height*1+1)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            
            #F = np.full_like(arg,500)
            inner_wall = print_layer(x, y, z,Feed = 1000)
            full_object.append(inner_wall)

            
            
            
            
            arg = np.linspace(0, np.pi*2,401)
            rad = [base_rad-3-0.5  for arg_i in arg]
            #rotation = rotation_calc(height)
            z = np.full_like(arg, height*1+1)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            

            layer_pos = np.column_stack([x, y, z])
            infill = line_fill(layer_pos,2.5,np.pi/4*(-1)**height)
            bottom = print_layer(infill[0], infill[1], infill[2],Feed = 1000)
            full_object.append(bottom)
            

            travel_point = travel_to(0,0,10)
            full_object.append(travel_point)


        
        

    return full_object

