import numpy as np
import math
import draw_object
import random
from scipy import interpolate
LAYER=2000


def spline3(x,y,point,deg):
    tck,u = interpolate.splprep([x,y],k=deg,s=0) 
    u = np.linspace(0,1,num=point,endpoint=True) 
    spline = interpolate.splev(u,tck)
    return spline[0],spline[1]


def y_calc(t,s):
    random_numbers = np.random.uniform(low=0, high=6, size=16).tolist()
    y= np.full_like(t,0)
    for i in range(4):
        for j in range(4):
            y+=random_numbers[4*i+j]*((t)**i)*((s)**j)
    return y



def object_modeling():
    pos_array=[]
    a_1=random.uniform(-1,1)
    a_2=random.uniform(-1,1)
    a_3=random.uniform(-1,1)
    a_4=random.uniform(-1,1)
    a_5=random.uniform(-1,1)
    a_6=random.uniform(-1,1)
    
    for height in range(LAYER):
        t = np.linspace(0,1,100)
        s = height / LAYER
        x = 100 * t  - 50
        z = np.full_like(x,0.2*height+0.2)
        
        y=[5*math.sin(t[i]*2*np.pi*2)*math.sin(s*2*np.pi*3) for i in range(len(t))]
        

        
        layer_pos = np.column_stack([x, y,z])
        pos_array.append(layer_pos.tolist())
        
       
        


        
        

    return pos_array

