import numpy as np
import math
import draw_object
import random
LAYER=500



def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        t = np.linspace(0,1,200)
        x = t*100-50
        #y = [2 * math.sin(i*2*np.pi*3) * 2*math.sin((height/LAYER)*2*np.pi*4) for i in t]
        y = [-6*math.floor( abs(1.05 * math.sin(i * 2 * np.pi * 20))) + 2 * math.sin(i*2*np.pi*2) * 2*math.sin((height/LAYER)*2*np.pi*2) for i in t]
        z = np.full_like(t, height*0.2+0.2)
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        
        
        x = np.array([50,50,-50,-50])
        y = np.array([0.4,10,10,0.4])
        z = np.full_like(x, height*0.2+0.2,dtype = np.float)
        
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        
        
        t = np.linspace(0,1,200)
        x = t*100-50
        #y = [2 * math.sin(i*2*np.pi*3) * 2*math.sin((height/LAYER)*2*np.pi*4) for i in t]
        y = [ 2 * math.sin(i*2*np.pi*2) * 2*math.sin((height/LAYER)*2*np.pi*2)+0.4 for i in t]
        z = np.full_like(t, height*0.2+0.2)
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        
        
        #pos_array.append([[50,-10.0,height*0.2+0.2]])
        pos_array.append([[25.0,10.0,height*0.2+0.2]])
        pos_array.append([[25.0,10.0,height*0.2+0.2],[25.0,0.4,height*0.2+0.2]])
        pos_array.append([[0.0,10.0,height*0.2+0.2]])
        pos_array.append([[0.0,10.0,height*0.2+0.2],[0.0,0.4,height*0.2+0.2]])
        pos_array.append([[-25.0,10.0,height*0.2+0.2]])
        pos_array.append([[-25.0,10.0,height*0.2+0.2],[-25.0,0.4,height*0.2+0.2]])
        pos_array.append([[-50.0,10.0,height*0.2+0.2]])
        pos_array.append([[-50.0,0,height*0.2+0.2]])

        


        
        

    return pos_array

