import math
import numpy as np
import gcoordinator as gc

LAYER = 100

full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, 2*np.pi, 100)
    x = 10 * np.cos(arg)
    y = 10 * np.sin(arg)
    z = np.full_like(arg, (height+1) * 0.2)
    wall = gc.Path(x, y, z)
    full_object.append(wall)

gc.gui_export(full_object)