import numpy as np
import math
import print_functions

LAYER=380
def rotation_calc(height):
    x=height/LAYER
    rotation=math.sin((x)*2.5*np.pi)
    return rotation*0.3

def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg=np.linspace(0,2*np.pi,481)
        rad=[22+ 4*math.floor(1.05*abs(np.sin(arg_i*40))) for arg_i in arg]
        if height/LAYER<=0.25:
            rad=[rad_i-5*(1-math.sin((height/LAYER)/0.25*np.pi/2)) for rad_i in rad]
        rotation = rotation_calc(height)

        x = rad*np.cos(arg+rotation)
        y = rad*np.sin(arg+rotation)
        z = np.full_like(arg, height*0.2+0.2)


        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        #draw_object.draw_line(x,y,z,w)
        #print(layer_pos)


        arg_c=np.linspace(0,-2*np.pi,201)
        rad_c=[22-0.25 for i in arg_c]
        if height/LAYER<=0.25:
            rad_c=[rad_i-5*(1-math.sin((height/LAYER)/0.25*np.pi/2)) for rad_i in rad_c]
        rotation = rotation_calc(height)
        x_c = rad_c*np.cos(arg_c+rotation)
        y_c = rad_c*np.sin(arg_c+rotation)
        z_c = np.full_like(arg_c, height*0.2+0.2)
        layer_pos_c = np.column_stack([x_c, y_c, z_c])
        pos_array.append(layer_pos_c.tolist())
        #draw_object.draw_line(x_c,y_c,z_c,w)
        if height<3 :
            offset = print_functions.contour_offset(layer_pos_c,-0.4)
            fill = print_functions.line_fill(offset,0.4)
            pos_array.append(fill)

        
    return pos_array
