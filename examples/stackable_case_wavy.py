# ==========================================================
# This code example is provided by @Mithril_MEX on X (twitter).
# https://twitter.com/Mithril_MEX
#
# Description: 
# This version, stackable_case, includes additional modifications:
# - Added skirt functionality
# - Adjusted initial phase (deltat)
# - Improved the quarter_func of the round function (now supports 'a' not being a power of 2)
# - Added undulations to the wall surface
# ==========================================================

import numpy as np
import gcoordinator as gc

LAYER=120
resolution = 200
nozzle = 0.4
thickness = 0.2

a = 4
L = 50
depth = 35
deltat = 2*np.pi*0.25
amp = 0.5
omega = 4*8

def quarter_func(arg):
    rad = L * (abs(np.cos(arg))**a + abs(np.sin(arg))**a)**(-1/a)
    return rad

full_object=[]

for height in range(LAYER):
    t = np.linspace(0+deltat, 2*np.pi+deltat, resolution)
    rad = quarter_func(t)
    base_x = rad * np.cos(t)
    base_y = rad * np.sin(t)
    thetaL = t*omega
    thetaH = height*omega*np.pi/LAYER
    ripple_x = amp*np.cos(thetaL)*np.sin(thetaH/4)
    ripple_y = amp*np.sin(thetaL)*np.sin(thetaH/4)
    x = base_x + ripple_x
    y = base_y + ripple_y
    z = np.full_like(x, thickness * (height +1))
    wall = gc.Path(x, y, z)
    wall.print_speed = 3000
    wall.extrusion_multiplier = 1.0

    if height == 0:
        inner_wall = gc.Transform.offset(wall, nozzle*8)
        inner_wall.print_speed = 1000
        inner_wall.extrusion_multiplier = 5.0
        full_object.append(inner_wall)

    if height>depth:
        wall = gc.Transform.offset(wall, nozzle*4)
    full_object.append(wall)

    for i in range(2):
        inner_wall = gc.Transform.offset(wall, -nozzle*(i+1))
        full_object.append(inner_wall)

    if height == depth or height == depth-1:
        offset = wall
        for i in range(4):
            offset = gc.Transform.offset(offset, nozzle)
            full_object.append(offset)

    if height <2:
        infill_wall = gc.Transform.offset(inner_wall, -nozzle)
        bottom = gc.line_infill(infill_wall,infill_distance = 2*nozzle, angle = np.pi/4+np.pi/2*height)
        full_object.append(infill_wall)
        full_object.append(bottom)

gc.gui_export(full_object)