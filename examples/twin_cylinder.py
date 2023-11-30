import numpy as np
import gcoordinator as gc

full_object = []
LAYER = 400
rad = 30

rot = np.pi/2
for height in range(LAYER):
    arg = np.linspace(0, np.pi, 100)
    x = rad * np.cos(arg)
    y = rad * np.sin(arg)
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    z = np.full_like(x, height * 0.2)
    wall_1 = gc.Path(x, y, z)
    wall_1 = gc.Transform.rotate_xy(wall_1, height/LAYER *rot)
    wall_1_inner = gc.Transform.offset(wall_1, -0.4)
    wall_1_inner.retraction = True
    wall_1_inner.z_hop = True
    
    full_object.append(wall_1)
    full_object.append(wall_1_inner)
    if height<6:
        base = gc.line_infill(wall_1, infill_distance=0.8, angle=np.pi/4+np.pi/2*height)
        full_object.append(base)

    arg = np.linspace(np.pi, 2*np.pi, 100)
    x = rad * np.cos(arg)
    y = rad * np.sin(arg)
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    z = np.full_like(x, height * 0.2)
    wall_2 = gc.Path(x, y, z)
    wall_2 = gc.Transform.rotate_xy(wall_2, height/LAYER *rot)
    wall_2 = gc.Transform.move(wall_2, -5,-5, 0)
    wall_2_inner = gc.Transform.offset(wall_2, -0.4)
    wall_2_inner.retraction = True
    wall_2_inner.z_hop = True

    full_object.append(wall_2)
    full_object.append(wall_2_inner)
    if height<6:
        base = gc.line_infill(wall_2, infill_distance=0.8, angle=np.pi/4+np.pi/2*height)
        full_object.append(base)

gc.gui_export(full_object)