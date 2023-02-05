import numpy as np
import math
#import draw_object
import print_functions
import parameter_curve_func as pf
from print_functions import *
'''
NOZZLE = 0.8
LAYER = 0.7
Print_speed = 700
Ext_multiplier = 1.4
'''

LAYER=50



def object_modeling():
    full_object=[]
    for height in range(LAYER):
        if height <2:
            arg = np.linspace(0, np.pi*2,401)
            rad = [30-1.9  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)
            #F = np.full_like(arg,500)

            
            layer_pos = print_layer(x, y, z)
            full_object.append(layer_pos)
            
            
            
            arg = np.linspace(0, np.pi*2,401)
            rad = [30-1.9-1+height*0.4  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)

            outer_circle = np.column_stack([x, y, z])
            fill = line_fill(outer_circle,2.4,np.pi/4*(-1)**height)
            
            fill_layer = print_layer(fill[0],fill[1],fill[2])
            full_object.append(fill_layer)
            
            
            
            
        t = np.linspace(0,1,203)
        arg = t * 2*np.pi
        height_list = (height + t)
        amp = 2+2*height_list/LAYER
        rad = 30 +amp*np.sin(arg*50.5+np.pi*height)+(height_list)


        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.linspace(height*0.7,(height+1)*0.7,203)

        layer_pos = print_layer(x, y, z)
        full_object.append(layer_pos)
        
        
        
        
       


        
        

    return full_object

