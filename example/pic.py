import numpy as np
import math
import draw_object
from print_functions import *
from open_cv_test import full_pic
LAYER=10
N = len(full_pic)
d =200/N


def object_modeling():
    full_object=[]
    for height in range(2):
        for k in range(N):
            if k%10 ==0:
                x = np.linspace(-100, 100,N)
                #y = np.full_like(x, 100- 50*k-d/2)
                y = np.array([full_pic[k][int(i)]/255*np.sin(i*np.pi/2)+100- d*k-d/2 for i in range(N)])
                z = np.full_like(x,height*0.1+0.05+0.8)
                line = print_layer(x, y, z)
                full_object.append(line)



        
        

    return full_object

