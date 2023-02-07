import numpy as np
import math
from print_functions import *


'''
NOZZLE = 0.4
layer height = 0.2
'''


LAYER=500

def function(height ,i):
    value = 4 * math.cos(math.sqrt((i*24-12)**2+(height/LAYER*24-12)**2))*math.exp(-((i*24-12)/10)**2-((height/LAYER*24-12)/10)**2)
    return value

def object_modeling():
    full_object=[]
    for height in range(LAYER):
        t = np.linspace(0,1,200)
        x = t*100-50
        #y = [2 * math.sin(i*2*np.pi*3) * 2*math.sin((height/LAYER)*2*np.pi*4) for i in t]
        y = [-6*math.floor( abs(1.05 * math.sin(i * 2 * np.pi * 20))) + function(height,i) for i in t]
        z = np.full_like(t, height*0.2+0.2)
        layer = print_layer(x, y, z)
        full_object.append(layer)

        
        t = np.linspace(0,1,200)
        x = t*100-50        
        y=[0.4+function(height,i) for i in t]
        z = np.full_like(t, height*0.2+0.2)
        wall = print_layer(x, y, z)
        full_object.append(wall)
        y_2=[0.8+function(height,i) for i in t]
        wall_2 = print_layer(x, y_2,  z)
        full_object.append(wall_2)
        

        
        
        

        


        
        

    return full_object

