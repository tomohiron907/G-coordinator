import numpy as np
import math
#import draw_object
import print_functions
import parameter_curve_func as pf

'''
NOZZLE = 0.8
LAYER = 0.4
Print_speed = 700
Ext_multiplier = 2.6
'''

LAYER=50





def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,203)
        amp = 2
        rad = 30+amp*np.sin(arg*50.5+np.pi*height) + 30*np.sin((height+arg/(2*np.pi))/LAYER*np.pi/2)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        #z = np.full_like(arg, height*0.7+0.7)
        z = np.linspace(height*0.7,(height+1)*0.7,203)
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())

        if height <2:
            arg = np.linspace(0, np.pi*2,401)
            rad = [30-2  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)
            #F = np.full_like(arg,500)

            layer_pos = np.column_stack([x, y, z])
            #pos_array.append(layer_pos.tolist())
            
            
            
            arg = np.linspace(0, np.pi*2,401)
            rad = [30-2-1  for arg_i in arg]
            #rotation = rotation_calc(height)
            x = rad*np.cos(arg )
            y = rad*np.sin(arg )
            z = np.full_like(arg, height*0.7+0.7)

            layer_pos = np.column_stack([x, y, z])
            offset = print_functions.line_fill(layer_pos,2.4,np.pi/4*(-1)**height)
            #pos_array.append(offset)


        
        

    return pos_array

