import numpy as np
import math
import draw_object
from print_functions import *
from open_cv_test import full_pic
LAYER=10
N = len(full_pic)
d =200/N


'''
NOZZLE = 0.8
layer = 0.4
E_mltp = 1.15

'''




def object_modeling():
    full_object=[]
    for height in range(2):
        arg = np.linspace(0, np.pi*2,5)
        rad = 100*math.sqrt(2)
        x = rad*np.cos(arg+np.pi/4)
        y = rad*np.sin(arg+np.pi/4)
        z = np.full_like(arg, height*0.4+0.4)
        layer = print_layer(x, y, z)
        full_object.append(layer)
        rect = np.column_stack([x, y, z])
        outer_offset = contour_offset(rect, -0.8)
        outer = print_layer(outer_offset[0], outer_offset[1], outer_offset[2])
        full_object.append(outer)
        
        inner_offset = contour_offset(rect, 0.6)
        ins = np.column_stack([inner_offset[0], inner_offset[1], inner_offset[2]])
        fill_inst = line_fill(ins, 0.8, np.pi/4*(-1)**height)
        fill = print_layer(fill_inst[0], fill_inst[1], fill_inst[2])
        full_object.append(fill)


        
        

    return full_object

