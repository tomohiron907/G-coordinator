

# Please execute this code after changing the machine setting's 
# kinematics to 'nozzle_tilt'.
# Author: @_gear_geek_'


import numpy as np
import math
import gcoordinator as gc
LAYER =50

full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,100)
    rad = 10
    x = rad*np.cos(arg)
    y = rad*np.sin(arg)
    z = np.full_like(arg, height*0.2+0.2)
    rot = arg
    tilt = [np.pi/2/100*height]*len(x)
    wall = gc.Path(x, y, z, rot, tilt)
    full_object.append(wall)

gc.gui_export(full_object)

