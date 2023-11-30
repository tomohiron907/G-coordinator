import numpy as np
import gcoordinator as gc

LAYER =400
nozzle = print

full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,100)
    rad = math.sqrt(50**2 - (height * 0.2-30)**2)
    x = rad*np.cos(arg)
    y = rad*np.sin(arg)
    z = np.full_like(arg, height*0.2+0.2)
    wall = gc.Path(x, y, z)
    outer_wall = gc.Transform.offset(wall, 0.4)
    infill = gc.gyroid_infill(wall, infill_distance = 6)
    full_object.append(infill)

gc.gui_export(full_object)

