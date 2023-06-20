import numpy as np
import math
import print_settings 
from path_generator import *
import matplotlib.pyplot as plt




a = 38
resolution = a*2
density = 4

x = np.linspace(-a , a , resolution)
y = np.linspace(-a , a , resolution)
z = np.linspace(-a , a , resolution*2)
X, Y, Z = np.meshgrid(x, y, z)
X /= density
Y /= density
Z /= density

# Equation for the Gyroid surface
equation =  np.cos(X) +  np.cos(Y) + np.cos(Z)


# Find intersection points
#slices = np.where(np.diff(np.sign(equation)))[0]

LAYER =5

def object_modeling():
    full_object=[]
    points_list = []  # List to store the points

    for height in range(resolution*2):
        slice_plane = equation[:, :, height]
        contours = plt.contour(x, y, slice_plane, levels=[0], colors='black')
        for contour in contours.collections:
            paths = contour.get_paths()
            for path in paths:
                points = path.vertices
                x_coords = points[:, 0]
                y_coords = points[:, 1]
                z_coords = np.full_like(x_coords, height/2)
                wall = Path(x_coords, y_coords, z_coords)
                full_object.append(wall)


    return full_object

