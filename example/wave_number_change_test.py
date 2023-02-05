import numpy as np
import math
#import draw_object
import print_functions
import parameter_curve_func as pf

'''
NOZZLE = 0.8
LAYER = 0.7
Print_speed = 700
Ext_multiplier = 1.4
'''

LAYER=40



def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        
            
            
            
        wave_number = 50.5-height
        t = np.linspace(0,1,int(wave_number*4+1))
        arg = t * 2*np.pi
        #height_list = (height + t)/LAYER
        #amp = 1.5+1.3*np.sin(height/LAYER*np.pi)
        amp = 2
        rad=30+amp*np.sin(arg*wave_number+np.pi*height)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.linspace(height*0.7,(height+1)*0.7,int(wave_number*4+1))
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        
        
        
        
       


        
        

    return pos_array

