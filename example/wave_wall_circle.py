import numpy as np
import math
from path_generator import *


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
        y = [-6*math.floor( abs(1.05 * math.sin(i * 2 * np.pi * 20))) + function(height,i) for i in t]
        z = np.full_like(t, height*0.2+0.2)
        layer = Path(x, y, z)
        full_object.append(layer)

        
        t = np.linspace(0,1,200)
        x = t*100-50        
        y=[0.4+function(height,i) for i in t]
        z = np.full_like(t, height*0.2+0.2)
        wall = Path(x, y, z)
        full_object.append(wall)
        wall_2 = Transform.offset(wall, -0.4)
        full_object.append(wall_2)
        

        
        
        

        


        
        

    return full_object

