import numpy as np
import gcoordinator as gc


LAYER =75



full_object=[]
for height in range(LAYER):
    arg = np.linspace(np.pi/4, np.pi/4+np.pi*2,5)
    rad = 70 
    x = rad*np.cos(arg)*1.618
    y = rad*np.sin(arg)
    z = np.full_like(arg, height*0.2+0.2)
    wall = gc.Path(x, y, z)
    inner_wall = gc.Transform.offset(wall, -0.7)
    infill = gc.gyroid_infill(wall,infill_distance = 8)
    wall.z_hop = False
    wall.retraction = False
    full_object.append(wall)
    full_object.append(inner_wall)
    full_object.append(infill)
            
gc.gui_export(full_object)
