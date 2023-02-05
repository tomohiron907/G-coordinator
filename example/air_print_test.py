import numpy as np
import math
import draw_object
import print_functions
from print_functions import print_layer,contour_offset
LAYER=25
d = 0.8
gr = 1.618



'''
NoZZLE = 0.4
LAYER = 0.2
speed = 650
ext = 1
'''
def object_modeling():
    full_object=[]
    for height in range(LAYER):
        
        x =np.array([80, -80,-80],dtype = float)
        y = np.array([-40,40,-40],dtype = float)
        z = np.full_like(x, height * 0.2 + 0.2)
        Z_line = np.column_stack([x,y,z])
        Z_offset = contour_offset(Z_line,0.2)
        layer = print_layer(Z_offset[0],Z_offset[1],Z_offset[2])
        full_object.append(layer)
        Z_offset_2 = contour_offset(Z_line,-0.2)
        layer = print_layer(Z_offset_2[0],Z_offset_2[1],Z_offset_2[2])
        full_object.append(layer)
        if height>= LAYER-2:
            for num in range(1,8):
               x = np.linspace(-80, -80+num * 20,10,dtype = float)
               
               y = np.full_like(x,40-num*10)
               z = np.full_like(x,height*0.2+0.2)
               layer = print_layer(x, y, z)
               full_object.append(layer)
        
      
        
   

    return full_object

