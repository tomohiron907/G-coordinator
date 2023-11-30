import numpy as np
import gcoordinator as gc

LAYER=100
base_rad = 50

full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,203)
    amp = 2
    rad = base_rad+amp*np.sin(arg*50.5+np.pi*height) 
    x = rad*np.cos(arg )
    y = rad*np.sin(arg )
    z = np.linspace(height*0.7,(height+1)*0.7,203)
    wave_wall = gc.Path(x, y, z)
    full_object.append(wave_wall)

    if height <2:
        arg = np.linspace(0, np.pi*2,401)
        rad = base_rad-2
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        z = np.full_like(arg, height*0.7+0.7)
        inner_wall = gc.Path(x, y, z)
        full_object.append(inner_wall)
        bottom = gc.line_infill(inner_wall, infill_distance = 1, angle = np.pi/4 + np.pi/2 *height)
        full_object.append(bottom)

        
gc.gui_export(full_object)

