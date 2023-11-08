import numpy as np
import gcoordinator as gc

LAYER =50
full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,100)
    rad = 10
    x = rad*np.cos(arg)
    y = rad*np.sin(arg)
    z = np.full_like(arg, height*0.2+0.2)
    wall, wall_2 = gc.Path(x, y, z), gc.Path(x, y, z)
    wall = gc.Transform.move(wall, pitch = np.pi/2)
    wall = gc.Transform.move(wall, x = 10)
    
    wall_2  =gc.Transform.move(wall_2, x = 10)
    wall_2 = gc.Transform.move(wall, pitch = np.pi/2)
    full_object.append(wall)
    full_object.append(wall_2)


gc.gui_export(full_object)
