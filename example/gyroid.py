import numpy as np
import math
import print_settings 
from path_generator import *
import matplotlib.pyplot as plt



#  parameters
#resolution = 40  # Resolution of the grid
a = 30
resolution = a*2
density = 3

x = np.linspace(-a , a , resolution)
x+=np.pi/2+0.5
y = np.linspace(-a , a , resolution)
y+=np.pi/2+0.5
z = np.linspace(-a , a , resolution*2)
X, Y, Z = np.meshgrid(x, y, z)


# Equation for the Gyroid surface
equation = np.sin(X/density) * np.cos(Y/density) + np.sin(Y/density) * np.cos(Z/density) + np.sin(Z/density) * np.cos(X/density)


# Find intersection points
#slices = np.where(np.diff(np.sign(equation)))[0]

LAYER =5

def object_modeling():
    full_object=[]
    '''for height in range(LAYER):
        x = np.array([10,-10,-10,10], dtype = float)
        y = np.array([10,10,-10,-10], dtype = float)
        z = np.full_like(x, height*0.2+0.2)
        layer = Path(x, y, z)
        full_object.append(layer)'''
    points_list = []  # List to store the points


    for height in range(resolution*2):
        # Choose the plane to slice (x-y plane in this case)
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

