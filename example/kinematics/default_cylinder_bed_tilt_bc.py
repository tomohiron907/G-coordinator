

# Please execute this code after changing the machine setting's 
# kinematics to 'bed_tilt_bc'.
# Author: @_gear_geek_'


import numpy as np
import math
import gcoordinator as gc

LAYER =50

full_object=[]
for height in range(LAYER):
    rad = 10
    x = [rad, rad]
    y = [0, 0]
    buf_z = height*0.2+0.2
    z = [buf_z, buf_z]
    rot = [math.pi*2*height, math.pi*2*(height+1)]
    tilt = [math.pi/4/LAYER*height, math.pi/4/LAYER*(height+1)]
    wall = gc.Path(x, y, z, rot, tilt)
    full_object.append(wall)        

gc.gui_export(full_object)