import numpy as np
import math


LAYER=280
def rotation_calc(height):
    ratio=height/LAYER
    rot_start=0.37
    rot_start_2=0.68
    if ratio<=0.3:
        rotation=0
    elif ratio>rot_start and ratio<=rot_start+0.12:
        rotation=-math.cos((ratio-rot_start)/0.12*np.pi)/2+1/2
    elif ratio>rot_start+0.12 and ratio<=rot_start_2:
        rotation=1
    elif ratio>rot_start_2 and ratio<=rot_start_2+0.12:
        rotation=-math.cos((ratio-rot_start_2)/0.12*np.pi+np.pi)/2+1/2
    else:
        rotation=0
    return rotation*(-0.25)

def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        
        if height/LAYER<0.2:
            for i in range(13):
                arg=np.linspace(0,2*np.pi,101)
                rad=[28.4-i*0.4+5*1.7**(-height/40)  for arg_i in arg]
                x = rad*np.cos(arg)
                y = rad*np.sin(arg)
                z = np.full_like(arg, height*0.3+0.3)
                layer_pos = np.column_stack([x, y, z])
                pos_array.append(layer_pos.tolist())
        else:
            arg=np.linspace(0,2*np.pi,361)
            rad=[24+ 4*math.floor(1.05*abs(np.sin(arg_i*30)))+5*1.7**(-height/40) for arg_i in arg]
            rotation=rotation_calc(height)
            x = rad*np.cos(arg+rotation)
            y = rad*np.sin(arg+rotation)
            z = np.full_like(arg, height*0.3+0.2)
            layer_pos = np.column_stack([x, y, z])
            pos_array.append(layer_pos.tolist())


            arg_c=np.linspace(0,2*np.pi,101)
            rad_c=[24-0.4 for arg_i in arg_c]
            rotation=rotation_calc(height)
            x_c = rad_c*np.cos(arg_c+rotation)
            y_c = rad_c*np.sin(arg_c+rotation)
            z_c = np.full_like(arg_c, height*0.3+0.2)
            layer_pos_c = np.column_stack([x_c, y_c, z_c])
            pos_array.append(layer_pos_c.tolist())


       
        #draw_object.draw_line(x_c,y_c,z_c,w)

        

        
    return pos_array
