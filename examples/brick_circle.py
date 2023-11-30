import numpy as np
import math
import gcoordinator as gc

LAYER=500
nozzle = 0.4
thickness = 0.2

N = 40

def brick(center):
    center_x = center[0]
    center_y = center[1]
    center_z = center[2]
    rotation = np.arctan2(center_y, center_x)
    brick_x = 4
    brick_y = 2
    brick_matrix = np.array([[-brick_x, brick_y], [brick_x, brick_y], [brick_x, -brick_y], [-brick_x, -brick_y], [-brick_x, brick_y]])
    rotation_matrix = np.array([[np.cos(-rotation), -np.sin(-rotation)], [np.sin(-rotation), np.cos(-rotation)]])
    brick_matrix = np.dot(brick_matrix, rotation_matrix)
    x = brick_matrix[:, 0] + center_x
    y = brick_matrix[:, 1] + center_y
    z = np.array([center_z]*5)
    wall = gc.Path(x, y, z)
    
    return wall
    
full_object=[]
for height in range(LAYER):
    if height%50<25:
        phase = 0
    else:
        phase = np.pi*2/N/2

    t = np.linspace(0, 2*np.pi, N)
    rad = 40
    x = rad * np.cos(t+phase)
    y = rad * np.sin(t+phase)
    z = np.full_like(x, thickness * (height+1)-0.1)
    for i in range(N):
        center = [x[i], y[i], z[i]]
        wall = brick(center)
        full_object.append(wall)
    
    if height<4:
        circle = gc.Path(x, y, z)
        circle = gc.Transform.offset(circle, -3)   
        infill = gc.line_infill(circle, infill_distance=1, angle=np.pi/4+np.pi/2*height)
        full_object.append(infill)


gc.gui_export(full_object)