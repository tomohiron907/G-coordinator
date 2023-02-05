import numpy as np
import math
import draw_object
import Gcode_process

LAYER=366
def rotation_calc(height):
    rotation=math.sin(height/LAYER*2.7*np.pi)
    '''if height/LAYER<0.15:
        rotation=math.sin(height/LAYER*100/15*np.pi/2)
    elif height/LAYER>=0.15 and height/LAYER<0.3:
        rotation=1
    elif height/LAYER>=0.3 and height/LAYER<0.7:
        rotation=math.sin(np.pi/2+(height/LAYER-0.3)/0.4*np.pi)
    elif height/LAYER>= 0.7 and height/LAYER<0.85:
        rotation=-1
    else:
        rotation=math.sin(np.pi*3/2+(height/LAYER-0.85)/0.15*np.pi/2)'''
    return rotation*0.5

def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg=np.linspace(0,2*np.pi,481)
        rad=[30+ 4*math.floor(1.05*abs(np.sin(arg_i*40))) for arg_i in arg]
        if height/LAYER>0.8:
            rad=[rad_i-8*(1-math.sin((1-height/LAYER)/0.2*np.pi/2)) for rad_i in rad]
        rotation = rotation_calc(height)

        x = rad*np.cos(arg+rotation)
        y = rad*np.sin(arg+rotation)
        z = np.full_like(arg, height*0.3+0.2)


        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        #draw_object.draw_line(x,y,z,w)
        #print(layer_pos)


        arg_c=np.linspace(0,2*np.pi,201)
        rad_c=[30-0.4 for i in arg_c]
        if height/LAYER>0.8:
            rad_c=[rad_i-8*(1-math.sin((1-height/LAYER)/0.2*np.pi/2)) for rad_i in rad_c]
        x_c = rad_c*np.cos(arg_c)
        y_c = rad_c*np.sin(arg_c)
        z_c = np.full_like(arg_c, height*0.3+0.2)
        layer_pos_c = np.column_stack([x_c, y_c, z_c])
        pos_array.append(layer_pos_c.tolist())
        #draw_object.draw_line(x_c,y_c,z_c,w)

        

        
    return pos_array
