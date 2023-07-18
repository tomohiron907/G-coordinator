# This code can slice and convert stl data into Gcode. 
# However, this function is still in beta version and its behavior is unstable. 
# For better performance, please wait for the next update.

import numpy as np
import math
import print_settings 
import trimesh
from path_generator import *
from infill_generator import *
from modeling_tool import slice
from console import *
import time


LAYER = 100 # Please edit this number according to the height of the STL file.
# If you specify a slice position higher than the height of the STL, an error will occur.

stl_path = 'PATH TO YOUR STL FILE'
mesh = trimesh.load(stl_path, merge_norm=True, merge_tex=True)


def object_modeling():
    full_object=[]
    start_time = time.time()
 #print(start_time)
    for height in range(LAYER):
        wall = slice(mesh, height*0.2)
        full_object.append(wall)
        print(f'slice time :{time.time() - start_time}')
        start_time = time.time()
    return full_object