import numpy as np
import math
import gcoordinator as gc


LAYER=56
nozzle = 0.4
thickness = 0.2

depth = 35



def quarter_func(arg, L):
    a = 4
    rad = L * (np.cos(arg)**a + np.sin(arg)**a)**(-1/a)
    return rad



full_object=[]
for height in range(LAYER):
    t = np.linspace(0, 2*np.pi, 200)
    rad = quarter_func(t, 40)
    x = rad * np.cos(t)
    y = rad * np.sin(t)
    z = np.full_like(x, thickness * (height +1))
    wall = gc.Path(x, y, z)
    full_object.append(wall)
    outer_wall = gc.Transform.offset(wall, 0.4)
    full_object.append(outer_wall)
    
    if height<6:
        x = 4.4 * np.cos(t)
        y = 4.4 * np.sin(t)
        z = np.full_like(x, thickness * (height +1))
        hole = gc.Path(x, y, z)
        full_object.append(hole)
        inner_hole = gc.Transform.offset(hole, -0.4)
        full_object.append(inner_hole)
        
        contour = gc.PathList([wall, hole])
        infill = gc.line_infill(contour, infill_distance = 0.5, angle = np.pi/4 + np.pi/2*height)
        infill.z_hop = True
        infill.retraction = True
        full_object.append(infill)
    elif height>=6 and height<57:
        
        t = np.linspace(0, 2*np.pi, 1000)
        L = 30 - 1.2-0.4+np.sqrt(10**2 - (height*0.2-10)**2)
        rad = quarter_func(t, L)
        if height<11:
            rad -= 2*np.floor(1.003*abs(np.cos(t*6)))
        x = rad * np.cos(t)
        y = rad * np.sin(t)
        z = np.full_like(x, thickness * (height +1))
        scale = gc.Path(x, y, z)
        full_object.append(scale)
        
        
        t = np.linspace(0, 2*np.pi, 200)
        L = 30 - 1.2+np.sqrt(10**2 - (height*0.2-10)**2)
        rad = quarter_func(t, L)
        x = rad * np.cos(t)
        y = rad * np.sin(t)
        z = np.full_like(x, thickness * (height +1))
        wall = gc.Path(x, y, z)
        full_object.append(wall)
        outer_wall = gc.Transform.offset(wall, 0.4)
        full_object.append(outer_wall)
        outer_wall = gc.Transform.offset(outer_wall, 0.4)
        full_object.append(outer_wall)
        
gc.gui_export(full_object)
        
    

