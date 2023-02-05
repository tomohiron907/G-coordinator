import numpy as np
import math
import draw_object
import random
from scipy import interpolate
LAYER=500


def spline3(x,y,point,deg):
    tck,u = interpolate.splprep([x,y],k=deg,s=0) 
    u = np.linspace(0,1,num=point,endpoint=True) 
    spline = interpolate.splev(u,tck)
    return spline[0],spline[1]


def object_modeling():
    pos_array=[]
    fit_x=[-50,-25,0,10,25,50]
    fit_y=[0,1,-2,2,6,0]
    fit_z=[0,25,50,65,100]
    fit_y_2=[0,1,0,-1,0]
    x,y = spline3(fit_x,fit_y,100,3)
    y_2,z = spline3(fit_y_2,fit_z,100,3)
    sp_x= np.array(x)
    sp_y = np.array(y)
    sp_y_2 = np.array(y_2)
    sp_z = np.array(z)
    for height in range(len(sp_z)):
        y_conb = []
        for seg in range(len(x)):
            y_conb.append(sp_y[seg] * sp_y_2[height]+2*sp_y[seg])
            
        y_conb = np.array(y_conb)
        
        z = np.full_like(x,sp_z[height])
        
        layer_pos = np.column_stack([sp_x, y_conb,z])
        pos_array.append(layer_pos.tolist())
        
       
        


        
        

    return pos_array

