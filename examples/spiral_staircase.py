import numpy as np
from tqdm import tqdm
import gcoordinator as gc

full_object = []
LAYER = 1000
band = np.pi/8
twist = 1.5 * np.pi
for height in tqdm(range(LAYER)):
    t = height/LAYER
    arg = np.linspace(0, 2*np.pi, 100)
    x = 20 * np.cos(arg)
    y = 20 * np.sin(arg)
    z = np.full_like(x, height * 0.2)
    center_pole = gc.Path(x, y, z)
    center_pole_2 = gc.Transform.offset(center_pole, -0.4)
    center_pole_2.z_hop = False
    center_pole_2.retraction = False
    full_object.append(center_pole_2)
    full_object.append(center_pole)
    if height<3:
        infill = gc.line_infill(center_pole, infill_distance = 2, angle =np.pi/4+np.pi/2*height)
        infill.retraction = False
        infill.z_hop = False
        #full_object.append(infill)

    arg = np.linspace(t*twist, t*twist+band, 20)
    arg_inv = np.linspace(t*twist+band, t*twist, 20)
    x = 60 * np.cos(arg)
    y = 60 * np.sin(arg)
    x_inv = 60.4 * np.cos(arg_inv)
    y_inv = 60.4 * np.sin(arg_inv)
    z = np.full_like(x, height * 0.2)
    wall = gc.Path(x, y, z)
    wall.z_hop = False
    wall.retraction = False
    outer_wall = gc.Path(x_inv, y_inv, z)
    wall_2 = gc.Transform.rotate_xy(wall, np.pi)
    wall_2.z_hop = False
    wall_2.retraction = False
    outer_wall_2 = gc.Transform.rotate_xy(outer_wall, np.pi)

    rot = int(t*twist*10)/10
    x = [60.4*np.cos(rot+band/2), 19.6*np.cos(rot+band/2)]
    y = [60.4*np.sin(rot+band/2), 19.6*np.sin(rot+band/2)]
    z = np.full_like(x, height * 0.2)
    bridge = gc.Path(x, y, z)
    bridge.print_speed = 3000
    bridge_2 = gc.Transform.rotate_xy(bridge, np.pi)
    bridge_2.print_speed = 3000

    full_object.append(wall)
    full_object.append(outer_wall)
    full_object.append(bridge)

    full_object.append(wall_2)
    full_object.append(outer_wall_2)
    full_object.append(bridge_2)

gc.gui_export(full_object)