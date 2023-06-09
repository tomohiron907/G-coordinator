import numpy as np
from path_generator import *
import print_settings

nozzle = print_settings.nozzle_diameter
thickness = print_settings.layer_height
#ext_multiplier = 1.2
LAYER = 2
def object_modeling():
    full_object=[]
    for height in range(LAYER):
        x = np.array([100,-100,-100,100,100], dtype = float)
        y = np.array([100,100,-100,-100,100], dtype = float)
        z = np.full_like(x, (height+1)*thickness)
        wall = Path(x, y, z)
        #infill = Transform.fill(wall, offset = - nozzle , infill_distance = nozzle , angle = np.pi/4 + np.pi/2 *height)
        infill = line_infill(wall, density = 1)
        full_object.append(wall)
        full_object.append(infill)
        
      
    return full_object