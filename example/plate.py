import numpy as np
import gcoordinator as gc

nozzle = 0.4
thickness = 0.2
LAYER = 2

full_object=[]
for height in range(LAYER):
    x = np.array([100,-100,-100,100,100], dtype = float)
    y = np.array([100,100,-100,-100,100], dtype = float)
    z = np.full_like(x, (height+1)*thickness)
    wall = gc.Path(x, y, z)
    infill = gc.line_infill(wall, infill_distance=0.4)
    full_object.append(wall)
    full_object.append(infill)
    
gc.gui_export(full_object)