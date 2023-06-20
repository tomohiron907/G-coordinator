import trimesh
import matplotlib.pyplot as plt
import path_generator

import numpy as np
# load mesh
#mesh = trimesh.load('cylinder_surface.stl', merge_norm=True, merge_tex=True)

# slice the mesh
def slice(mesh, z_height):

    slice = mesh.section_multiplane(plane_origin=[0, 0, 0], plane_normal=[0, 0, 1], heights=[z_height])

    s = slice[0]
    path_num = len(s.discrete)
    path_list = []
    for i in range(path_num):
        points = s.discrete[i]
        plt.plot(*points.T)
        
        coords = points.T
        x = np.array(coords[0])
        y = np.array(coords[1])
        z = np.full_like(x, z_height)
        path = path_generator.Path(x, y, z)
        path_list.append(path)

    path_list = path_generator.PathList(path_list)
    return path_list

