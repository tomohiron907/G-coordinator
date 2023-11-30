import numpy as np
import gcoordinator as gc

LAYER=60
base_rad = 80


full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,403)
    amp = 2
    z = np.linspace(height*1,(height+1)*1,403)
    rad = base_rad
    rad += 7*np.sin((z/LAYER)*np.pi)
    x = rad*np.cos(arg )
    y = rad*np.sin(arg )
    circle = gc.Path(x, y, z)
    
    
    rad+=amp*np.sin(arg*100.5+np.pi*height)
    x = rad*np.cos(arg )
    y = rad*np.sin(arg )
    wave_wall = gc.Path(x, y, z)
    full_object.append(wave_wall)
    
    if height<2:
        inner_wall = gc.Transform.offset(circle, -2)
        full_object.append(inner_wall)
        bottom = gc.line_infill(inner_wall, infill_distance = 2, angle = np.pi/4 + np.pi/2*height)
        full_object.append(bottom)
        


gc.gui_export(full_object)
