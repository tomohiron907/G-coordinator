import numpy as np
import gcoordinator as gc


LAYER=110
base_rad = 35


def wave(x):
    y = np.arccos(np.cos(x + np.pi/2))/np.pi * 2 -1
    return y

full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, np.pi*2,203)
    amp = 3
    z = np.linspace(height*1,(height+1)*1,203)
    rad = base_rad
    off_rad = 8
    
    if height < LAYER* 0.175:
        rad += 0
        rad += off_rad*np.sin((z/LAYER) * 5*np.pi/2)
    else:
        rad += amp*np.sin(arg*50.5+height*np.pi)+off_rad
        b = 6 * np.sin((z / LAYER-0.175) * np.pi * 3.5  )
        a = 3
        rad += b * np.sin(a * arg)
    x = rad*np.cos(arg )
    y = rad*np.sin(arg )
    wave_wall = gc.Path(x, y, z)
    full_object.append(wave_wall)
    


    if height <2:
        arg = np.linspace(0, np.pi*2,401)
        rad = base_rad-0.7
        z = np.full_like(arg, height*1+1)
        x = rad*np.cos(arg )
        y = rad*np.sin(arg )
        
        inner_wall = gc.Path(x, y, z)
        full_object.append(inner_wall)
        bottom = gc.line_infill(inner_wall, infill_distance = 1, angle = np.pi/4+ np.pi/2 * height)
        full_object.append(bottom)


gc.gui_export(full_object)
