import numpy as np
import gcoordinator as gc

LAYER=120
nozzle = 0.4
thickness = 0.2
a = 4
L = 40
depth = 35


def quarter_func(arg):
    rad = L * (np.cos(arg)**a + np.sin(arg)**a)**(-1/a)
    return rad

full_object=[]
for height in range(LAYER):
    t = np.linspace(0, 2*np.pi, 200)
    rad = quarter_func(t)
    x = rad * np.cos(t)
    y = rad * np.sin(t)
    z = np.full_like(x, thickness * (height +1))
    wall = gc.Path(x, y, z)
    
    if height>depth:
        wall = gc.Transform.offset(wall, nozzle*4)
    full_object.append(wall)
    
    for i in range(2):
        inner_wall = gc.Transform.offset(wall, -nozzle*(i+1))
        full_object.append(inner_wall)
        
    if height == depth or height == depth-1:
        offset = wall
        for i in range(4):
            offset = gc.Transform.offset(offset, nozzle)
            full_object.append(offset)
            
    if height <2:
        infill_wall = gc.Transform.offset(inner_wall, -nozzle)
        infill_wall.z_hop = True
        infill_wall.retraction = True
        bottom  = gc.line_infill(infill_wall, infill_distance = 2*nozzle, angle = np.pi/4 + np.pi/2*height)
        bottom.z_hop = True
        bottom.retraction = True
        full_object.append(infill_wall)
        full_object.append(bottom)
    

gc.gui_export(full_object)

