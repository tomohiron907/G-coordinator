import numpy as np
import math
import print_settings 
from path_generator import *
import matplotlib.pyplot as plt



def eq_to_path(fn,height, x_min=-10, x_max=10, y_min=-10, y_max=10, z_min=0, z_max=10,   x_resolution = 200, y_resolution = 200, z_resolution = 200, val = 0):


    x = np.linspace(x_min , x_max , x_resolution)
    y = np.linspace(y_min , y_max , y_resolution)
    z = np.linspace(z_min , z_max , z_resolution)
    

    # Equation for the Gyroid surface
    #equation = np.sin(X) * np.cos(Y) + np.sin(Y) * np.cos(Z) + np.sin(Z) * np.cos(X)
    X, Y, Z = np.meshgrid(x, y, z)
    equation = fn(X, Y, Z)
    path_list_buffer = []
    #for height in range(z_min, z_max):
    slice_plane = equation[:, :, height]
    contours = plt.contour(x, y, slice_plane, levels=[0], colors='black')
    for contour in contours.collections:
        paths = contour.get_paths()
        for path in paths:
            points = path.vertices
            x_coords = points[:, 0]
            y_coords = points[:, 1]
            z_coords = np.full_like(x_coords, height*0.2)
            wall = Path(x_coords, y_coords, z_coords)
            path_list_buffer.append(wall)
    return PathList(path_list_buffer)


