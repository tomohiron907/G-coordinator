import numpy as np
import math
import draw_object
import print_functions
from print_functions import print_layer,contour_offset
LAYER=80
d = 1
gr = 1.618



'''
NoZZLE = 0.4
LAYER = 0.2
speed = 4000
ext = 1.85
'''
full_object=[]

def bridge_line(x_start, x_end, y_start, y_end, height):
    global full_object
    x = gr*np.linspace(x_start, x_end,10)
    y = np.linspace(y_start,y_end,10)
    z = np.full_like(x,height*0.2+0.2)
    line = np.column_stack([x, y, z])
    layer = print_layer(x, y, z)
    full_object.append(layer)
    offset = contour_offset(line, 0.2)
    offset_layer = print_layer(offset[0], offset[1], offset[2])
    full_object.append(offset_layer)


def object_modeling():
    global full_object
    for height in range(LAYER):
        
        x =gr*np.array([40, 40, -40,-40],dtype = float)
        y = np.array([40,-40,40,-40],dtype = float)
        z = np.full_like(x, height * 0.2 + 0.2)
        Z_line = np.column_stack([x,y,z])
        Z_offset = contour_offset(Z_line,0.2)
        layer = print_layer(Z_offset[0],Z_offset[1],Z_offset[2])
        full_object.append(layer)
        Z_offset_2 = contour_offset(Z_line,-0.2)
        layer = print_layer(Z_offset_2[0],Z_offset_2[1],Z_offset_2[2])
        full_object.append(layer)
        
        
        if height != 0 and height %3 ==0:
            bridge_line(40, 40-d*height, 40-d*height, -40+d*height,height)
            
          
            bridge_line(-40, -40+d*height, -40+d*height, +40-d*height,height)
            
            
            
            
        if height != 0 and height %3 ==1:
            bridge_line(40, 40-d*(height-1), 40-d*(height-1), -40+d*(height-1),height)
            
            
           
            bridge_line(-40, -40+d*(height-1), -40+d*(height-1), +40-d*(height-1),height)
        
   

    return full_object

