'''
NOZZLE = 0.4
layer height = 0.2
'''


import numpy as np
import math
import draw_object
import random
import print_functions
LAYER=500

def function(height ,i):
    value = 4 * math.cos(math.sqrt((i*24-12)**2+(height/LAYER*24-12)**2))*math.exp(-((i*24-12)/10)**2-((height/LAYER*24-12)/10)**2)
    return value

def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        t = np.linspace(0,1,200)
        x = t*100-50
        #y = [2 * math.sin(i*2*np.pi*3) * 2*math.sin((height/LAYER)*2*np.pi*4) for i in t]
        y = [-6*math.floor( abs(1.05 * math.sin(i * 2 * np.pi * 20))) + function(height,i) for i in t]
        z = np.full_like(t, height*0.2+0.2)
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        
        
        '''x = np.array([50,50,-50,-50])
        y = np.array([0.4,10,10,0.4])
        z = np.full_like(x, height*0.2+0.2,dtype = np.float)
        
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())'''
        
        
        t = np.linspace(0,1,200)
        x = t*100-50
        #y = [2 * math.sin(i*2*np.pi*3) * 2*math.sin((height/LAYER)*2*np.pi*4) for i in t]
         
        y=[0.4+function(height,i) for i in t]
        z = np.full_like(t, height*0.2+0.2)
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        offset = print_functions.contour_offset(layer_pos,0.4)
        pos_array.append(offset)
        if height == 0 :
            for i in range(15):
                offset = print_functions.contour_offset(layer_pos,0.4+0.4*i)
                pos_array.append(offset)
        
        
        

        


        
        

    return pos_array

