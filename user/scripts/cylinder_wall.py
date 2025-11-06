import numpy as np
import gcoordinator as gc

full_object=[]
for height in range(100):
    angle = np.linspace(0, 2*np.pi, 100)
    x = 10 * np.cos(angle)
    y = 10 * np.sin(angle)
    z = np.full_like(angle, (height+1) * 0.2)
    wall = gc.Path(x, y, z)
    full_object.append(wall)

gc.gui_export(full_object)