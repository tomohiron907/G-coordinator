import numpy as np
import gcoordinator as gc

LAYER=50

full_object=[]
for height in range(LAYER):
    x = np.array([10,-10,-10,10, 10], dtype = float)
    y = np.array([10,10,-10,-10, 10], dtype = float)
    z = np.full_like(x, height*0.2+0.2)
    layer = gc.Path(x, y, z)

    full_object.append(layer)

gc.gui_export(full_object)
