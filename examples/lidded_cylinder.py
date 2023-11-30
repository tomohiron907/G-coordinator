import numpy as np
import gcoordinator as gc

LAYER=50

full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,100)
    rad = 30
    x = rad*np.cos(arg)
    y = rad*np.sin(arg)
    z = np.full_like(arg, height*0.4+0.4)
    layer = gc.Path(x,y,z)
    full_object.append(layer)
    offset = gc.Transform.offset(layer, 0)
for i in range(70):
    offset = gc.Transform.offset(offset, - 0.4)
    full_object.append(offset)

gc.gui_export(full_object)
