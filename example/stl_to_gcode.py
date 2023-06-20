import numpy as np
import math
import print_settings 
import trimesh
from path_generator import *
from infill_generator import *
from stl_slice import *
from tqdm import tqdm

LAYER = 150 # Please edit this number according to the height of the STL file.
# If you specify a slice position higher than the height of the STL, an error will occur.

stl_path = 'PATH TO YOUR STL FILE'
mesh = trimesh.load(stl_path, merge_norm=True, merge_tex=True)


def object_modeling():
    full_object=[]
    
    for height in tqdm(range(LAYER)):
        wall = slice(mesh, height*0.2)
        full_object.append(wall)

        if height<5:
            infill = line_infill(wall, density = 1)
            full_object.append(infill)
        else:
            infill = line_infill(wall, density = 0.9, angle = np.pi/2*height+np.pi/4)
            full_object.append(infill)
        

    return full_object

