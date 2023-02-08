import numpy as np
import math
import parameter_curve_func as pf
from print_functions import *
'''
NOZZLE = 0.8
LAYER = 0.7
Print_speed = 700
Ext_multiplier = 1.4
'''

LAYER=120



def object_modeling():
    full_object=[]
    for height in range(LAYER):
        if height <2:
            arg = np.linspace(0, np.pi*2,401)
            rad = [30-1  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)
            #F = np.full_like(arg,500)

            layer = print_layer(x, y, z)
            full_object.append(layer)
            
            
            
            arg = np.linspace(0, np.pi*2,401)
            rad = [30-1-1+height*0.4  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)
            #layer_pos = np.column_stack([x, y, z])
            F = np.full_like(arg,15)
            
            outer_circle = np.column_stack([x, y, z])
            fill = line_fill(outer_circle,2.4,np.pi/4*(-1)**height)
            
            fill_layer = print_layer(fill[0],fill[1],fill[2])
            full_object.append(fill_layer)
            
            
            full_object.append([[0,0,10]])
            
            
            
            
        t = np.linspace(0,1,203)
        arg = t * 2*np.pi
        height_list = (height + t)/LAYER
        
        bezier_rad =np.array( [30 * pf.function(height_list_i/1.01) for height_list_i in height_list])
        amp = 1+4.5*np.exp(-(12*(height/LAYER-1/2.8))**2)
        rad=30+amp*np.sin(arg*50.5+np.pi*height)+ bezier_rad
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.linspace(height*0.7,(height+1)*0.7,203)
        layer = print_layer(x, y, z)
        full_object.append(layer)
        
        
        
        
       


        
        

    return full_object

