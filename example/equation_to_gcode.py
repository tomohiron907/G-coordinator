import numpy as np
from path_generator import *
from modeling_tool import eq_to_path


def equation(x, y, z):
    gyroid = np.sin(x) * np.cos(y) + np.sin(y) * np.cos(z) + np.sin(z) * np.cos(x)
    return gyroid

    
def object_modeling():
    full_object=[]


    x_min, x_max = -10, 10
    y_min, y_max = -10, 10
    z_min, z_max = 0, 30
    for height in range(1):
        path = eq_to_path(equation, height)
        full_object.append(path)
    return full_object
    
    