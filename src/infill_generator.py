import sys
import numpy as np
import math
from print_settings     import *
from matplotlib.path    import Path as matlabPath
from path_generator     import Path, PathList
from window.main_window import *
import print_settings
import matplotlib.pyplot as plt
"""
G-coordinator has two infill generators: gyroid and line infill.

you can make your own infill generator by changing the equation below.
equation = np.sin(X/density + Y/density*np.tan(angle))

"""


def gyroid_infill(path, density=0.5, value=0):
    """
    generate gyroid infill

    args    : Path or PathList
    returns : PathList of gyroid

    usage   : infill = gyroid_infill(path, density=0.9, value=0)
    """
    if isinstance(path, Path):
        path_list = PathList([path])
    elif isinstance(path, PathList):
        path_list = path
    # Set initial values
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')

    # Examine the coordinate sequence of each path object and
    #  update the minimum and maximum values
    for path in path_list.paths:
        x_coords = path.x
        y_coords = path.y
        if len(x_coords)>0:
            min_x = min(min_x, min(x_coords))
            max_x = max(max_x, max(x_coords))
            resolution_x = int((max_x-min_x)/0.4)
        if len(y_coords)>0:
            min_y = min(min_y, min(y_coords))
            max_y = max(max_y, max(y_coords))
            resolution_y = int((max_y - min_y)/0.4)
    z_height = path_list.paths[0].center[2]
    # Grid parameters
    # Resolution of the grid
    x = np.linspace(min_x, max_x, resolution_x)
    y = np.linspace(min_y, max_y, resolution_y)
    X, Y = np.meshgrid(x, y)
    density = -9.9 * density + 10
    # Equation for the Gyroid surface
    theta = np.pi/4
    equation = np.sin(X/density*np.cos(theta) + Y/density*np.sin(theta)) * np.cos(-X/density*np.sin(theta) + Y/density*np.cos(theta)) + np.sin(-X/density*np.sin(theta) + Y/density*np.cos(theta)) * np.cos(z_height/density) + np.sin(z_height/density) * np.cos(X/density*np.cos(theta) + Y/density*np.sin(theta))-value
    insides = []
    for path in path_list.paths:
        x_list = path.x
        y_list = path.y        
        # Determine the inside region
        inside = np.ones_like(equation) # outside = 1
        path = matlabPath(np.column_stack([x_list, y_list]))
        
        points = np.column_stack((X.flatten(), Y.flatten()))
        inside = path.contains_points(points) # inside = 0
        inside = inside.reshape(X.shape).astype(float)
        inside[inside == 1] = -1 # change inside to -1
        inside[inside == 0] = 1  # Change outside  to 1
        insides.append(inside)

    result = insides[0]  # Set the first ndarray as the initial value

    for i in range(1, len(insides)):
        result = np.multiply(result, insides[i])  # Calculate the Adamar product

    # Replace -1 with np.nan
    result[result == 1] = np.nan

    # Plot the slices
    slice_plane = equation * result
    contours = plt.contour(x, y, slice_plane, levels=[0], colors='black')
    
    infill_path_list = []
    for contour in contours.collections:
        paths = contour.get_paths()
        for path in paths:
            points = path.vertices
            x_coords = points[:, 0]
            y_coords = points[:, 1]
            z_coords = np.full_like(x_coords, z_height)
            wall = Path(x_coords, y_coords, z_coords)
            infill_path_list.append(wall)
    
    return PathList(infill_path_list)


def line_infill(path, density=0.5, angle=np.pi/4):
    """
    generate line infill

    args    : Path or PathList 
    returns : PathList of line infill

    usage   : infill = line_infill(path, density=0.9, angle=np.pi/4)
    """
    if isinstance(path, Path):
        path_list = PathList([path])
    elif isinstance(path, PathList):
        path_list = path


    x_coords = np.concatenate([path.x for path in path_list.paths if len(path.x) > 0])
    y_coords = np.concatenate([path.y for path in path_list.paths if len(path.y) > 0])
    min_x = np.min(x_coords) if len(x_coords) > 0 else float('inf')
    max_x = np.max(x_coords) if len(x_coords) > 0 else float('-inf')
    min_y = np.min(y_coords) if len(y_coords) > 0 else float('inf')
    max_y = np.max(y_coords) if len(y_coords) > 0 else float('-inf')

    
    z_height = path_list.paths[0].center[2]
    # Grid parameters
    # Resolution of the grid
    x = np.linspace(min_x, max_x, 250)
    y = np.linspace(min_y, max_y, 250)
    X, Y = np.meshgrid(x, y)
    density = -9.9 * density + 10
    # Equation for the Gyroid surface
    equation = np.sin(X/density + Y/density*np.tan(angle))
    insides = []
    for path in path_list.paths:
        x_list = path.x
        y_list = path.y        
        # Determine the inside region
        inside = np.ones_like(equation) # outside = 1
        path = matlabPath(np.column_stack([x_list, y_list]))
        
        points = np.column_stack((X.flatten(), Y.flatten()))
        inside = path.contains_points(points) # inside = 0
        inside = inside.reshape(X.shape).astype(float)
        inside[inside == 1] = -1 # change inside to -1
        inside[inside == 0] = 1  # Change outside  to 1
        insides.append(inside)

    result = insides[0]  

    for i in range(1, len(insides)):
        result = np.multiply(result, insides[i])  

    # Replace -1 with np.nan
    result[result == 1] = np.nan

    # Plot the slices
    slice_plane = equation * result
    contours = plt.contour(x, y, slice_plane, levels=[0], colors='black')
    
    infill_path_list = []
    for contour in contours.collections:
        paths = contour.get_paths()
        for path in paths:
            points = path.vertices
            x_coords = points[:, 0]
            y_coords = points[:, 1]
            z_coords = np.full_like(x_coords, z_height)
            wall = Path(x_coords, y_coords, z_coords)
            infill_path_list.append(wall)
    return PathList(infill_path_list)