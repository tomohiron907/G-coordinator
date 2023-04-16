import numpy as np
import math
from print_functions import *
LAYER=100
d = 0.8
gr = 1/1.618



'''
NoZZLE = 0.4
LAYER = 0.2
speed = 650
ext = 1
'''
def object_modeling():
    full_object=[]
    for height in range(LAYER):
        arg = np.linspace(np.pi/4, np.pi*9/4,5)
        rad = 40*math.sqrt(2)
        x = rad*np.cos(arg)
        y = gr*rad*np.sin(arg)
        z = np.full_like(arg, height*0.2+0.2)
        layer = Path(x, y, z)
        full_object.append(layer)
        
        rad = 40.4*math.sqrt(2)
        x = rad*np.cos(arg)
        y = gr*rad*np.sin(arg)
        z = np.full_like(arg, height*0.2+0.2)
        layer = Path(x, y, z)
        full_object.append(layer)
        
        
        x = np.linspace(-40,40,10)
        y = gr*np.linspace(40,-40,10)
        z = np.full_like(x, height * 0.2 + 0.2)
        
        layer = Path(x,  y , z)
        full_object.append(layer)
        
        
        if height != 0 and height %3 ==0:
            x = np.linspace(40, 40-d*height,10)
            y = gr*np.linspace(40-d*height,-40+d*height,10)
            z = np.full_like(x,height*0.2+0.2)
            layer = Path(x, y, z)
            full_object.append(layer)
            
            x = np.linspace(-40, -40+d*height,10)
            y = gr*np.linspace(-40+d*height,+40-d*height,10)
            z = np.full_like(x,height*0.2+0.2)
            layer = Path(x, y, z)
            full_object.append(layer)
            
        if height != 0 and height %3 ==1:
            x = np.linspace(40, 40-d*(height-1),10)
            y = gr*np.linspace(40-d*(height-1),-40+d*(height-1),10)
            z = np.full_like(x,(height)*0.2+0.2)
            layer = Path(x, y, z)
            full_object.append(layer)
            
            x = np.linspace(-40, -40+d*(height-1),10)
            y = gr*np.linspace(-40+d*(height-1),+40-d*(height-1),10)
            z = np.full_like(x,(height)*0.2+0.2)
            layer = Path(x, y, z)
            full_object.append(layer)
        
   

    return full_object

