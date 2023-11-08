import numpy as np
import  gcoordinator as gc

LAYER=50
N = 6 #polygon number


full_object = []
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,N+1)
    rad = 25
    x = rad*np.cos(arg)
    y = rad*np.sin(arg)
    z = np.full_like(arg, height*0.2+0.2)
    wall = gc.Path(x, y, z)
    full_object.append(wall)
    if height==0:
        bottom = gc.line_infill(wall, infill_distance = 0.4)
        full_object.append(bottom)

gc.gui_export(full_object)
