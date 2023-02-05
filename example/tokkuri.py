import numpy as np
import math
import draw_object
import Gcode_process

LAYER=400
def rotation_calc(height):
        rotation=math.sin(height/LAYER*2.2*np.pi)
        return(rotation)

def object_modeling():
    pos_array=[]
    for height in range(LAYER):
        arg = np.linspace(0, np.pi*2,301)
        rad = [32-4*(height)/100 + 4*math.floor(1.05*abs(np.sin(arg_i*25))) + (LAYER-height)/LAYER*10*math.sin(height/LAYER*2*np.pi*0.8)-height/LAYER*8 -(LAYER-height)/LAYER*10 for arg_i in arg]
        rotation=rotation_calc(height)
        x = rad*np.cos(arg+rotation)
        y = rad*np.sin(arg+rotation)
        z = np.full_like(arg, height*0.3+0.2)
        layer_pos = np.column_stack([x, y, z])
        pos_array.append(layer_pos.tolist())
        #draw_object.draw_line(x,y,z,w)
        #print(layer_pos)



        arg_c = np.linspace(0, np.pi*2,200)
        rad_c = [32-0.4-4*(height)/100 + (LAYER-height)/LAYER*10*math.sin(height/LAYER*2*np.pi*0.8)-height/LAYER*8 -(LAYER-height)/LAYER*10 for arg_i in arg_c]
        x_c = rad_c*np.cos(arg_c+height/100*np.pi/2)
        y_c = rad_c*np.sin(arg_c+height/100*np.pi/2)
        z_c = np.full_like(arg_c, height*0.3+0.2)


        layer_pos_c = np.column_stack([x_c, y_c, z_c])
        pos_array.append(layer_pos_c.tolist())
        #draw_object.draw_line(x_c,y_c,z_c,w)

        
    return pos_array
