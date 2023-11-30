import gcoordinator as gc
import numpy as np

full_object = []
p_1 = 20
P_2 = 20
rad_1 = 20
rad_2 = 15
rad_3 = 10
for layer in range(50):
    theta = np.linspace(0, 2*np.pi, 1000)
    x = rad_1 * np.cos(theta) + rad_2 * np.cos(p_1*theta) + rad_3 * np.cos(P_2*theta)
    y = rad_1 * np.sin(theta) + rad_2 * np.sin(p_1*theta) + rad_3 * np.sin(P_2*theta)
    z = np.full_like(x, layer * 0.2)
    wall = gc.Path(x, y, z )
    full_object.append(wall)

gc.gui_export(full_object)