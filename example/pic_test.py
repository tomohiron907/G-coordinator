import numpy as np
import math
import draw_object
from print_functions import *
from open_cv_test import full_pic
LAYER=10
N = len(full_pic)
d =200/N


'''
NOZZLE = 0.2
layer = 0.1
speed = 800
un/ retraction = 3.5
e_mltp = 1.2
'''



def object_modeling():
    full_object=[]
    for height in range(5):
        for k in range(20):
            x = np.linspace(-25, 25,40)
            y = np.array([25- k*2.5+np.sin(i/40*2*np.pi*10) for i in range(40)])
            z = np.full_like(x, 0.1* height + 0.07+0.8)
            line = print_layer(x, y, z)
            full_object.append(line)


        
        

    return full_object

