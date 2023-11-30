import numpy as np
import gcoordinator as gc

LAYER=80
nozzle = 0.4
thickness = 0.2
a = 4
L = 40


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
    full_object.append(wall)
    outer_wall = gc.Transform.offset(wall, 0.4)
    full_object.append(outer_wall)
    
    if height<20:
        gyroid = gc.gyroid_infill(wall, infill_distance = 2)
        full_object.append(gyroid)
    
gc.gui_export(full_object)

