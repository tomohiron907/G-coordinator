import numpy as np
import math
from print_functions import *
LAYER=20

def print_rectangle (height):
    x = np.array([50,-50,-50,50,50],dtype = float)
    y = np.array([25,25,-25,-25,25],dtype = float)
    z = np.full_like(x, height*0.2+0.2)
    layer = print_layer(x, y, z)
    coords = np.column_stack([x, y, z])
    return layer

def print_line(start_x, start_y, end_x, end_y,height):
    x = np.linspace(start_x, end_x, 30)
    y = np.linspace(start_y, end_y, 30)
    z = np.full_like(x, height*0.2+0.2)
    layer = print_layer(x, y, z, Feed = 400, E_multiplier = 2)
    return layer

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        rectangle= print_rectangle(height)
        full_object.append(rectangle)
        offset = contour_offset(rectangle,0.4)
        offset_line = print_layer(offset[0], offset[1], offset[2])
        full_object.append(offset_line)

    for i in range(10):
        line = print_line(-50,25-i*5, -50+i*5, 25,20)
        full_object.append(line)
    for i in range(10):
        line = print_line(-50+i*5,-25, i*5, 25,20)
        full_object.append(line)
    for i in range(10):
        line = print_line(i*5,-25, 50, 25-i*5,20)
        full_object.append(line)
        
    for i in range(10):
        line = print_line(-50,-25+i*5, -50+i*5, -25,20)
        full_object.append(line)
    for i in range(10):
        line = print_line(-50+i*5,25, i*5, -25,20)
        full_object.append(line)
    for i in range(10):
        line = print_line(i*5,25, 50, -25+i*5,20)
        full_object.append(line)
    
    
    rectangle_top = print_rectangle(20)
    full_object.append(rectangle_top)
    
    for i in range(20):
        y = np.linspace(25,-25,100)
        x = np.full_like(y, 5*i-50)
        z = np.full_like(y, 4.4)
        line = print_layer(x, y, z, Feed = 400, E_multiplier = 4)
        full_object.append(line)
    
    for i in range(10):
        x = np.linspace(-50,50,100)
        y = np.full_like(x, 5*i-25-0.25)
        z = np.full_like(x, 4.4)
        line = print_layer(x, y, z, Feed = 400, E_multiplier = 4)
        full_object.append(line)
    
    rectangle_top = print_rectangle(22)
    full_object.append(rectangle_top)
    
    return full_object

