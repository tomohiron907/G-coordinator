import numpy as np
import gcoordinator as gc

LAYER =50

full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,100)
    rad = 10
    x = rad*np.cos(arg)
    y = rad*np.sin(arg)
    z = np.full_like(arg, height*0.2+0.2)
    wall = gc.Path(x, y, z)
    outer_wall = gc.Transform.offset(wall, 0.4)
    full_object.append(wall)
    full_object.append(outer_wall)
    
    if height <2 :
        bottom = gc.line_infill(wall, infill_distance = 0.4, angle = np.pi/4 + np.pi/2*height)
        #bottom = gc.Transform.rotate_xy(bottom, np.pi/2*height)
        bottom.print_speed = 400
        bottom.z_hop = True
        bottom.retraction = True
        full_object.append(bottom)

gc.gui_export(full_object)
