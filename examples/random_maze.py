import random
import numpy as np
import gcoordinator as gc

nozzle = 0.4
thickness = 0.2

LAYER = 20
s = 10
def line(x_pos, y_pos, a):
    if a:
        x = np.array([x_pos*s, x_pos*s+s], dtype = float)
        y = np.array([y_pos*s, y_pos*s+s], dtype = float)
        return x-100, y-100
    else:
        x = np.array([x_pos*s, x_pos*s+s], dtype = float)
        y = np.array([y_pos*s+s, y_pos*s], dtype = float)
        return x-100, y-100


full_object=[]
random_slope = [[  bool(random.getrandbits(1))   for j in range(20)] for j in range(20)]
for height in range(LAYER):
    for i in range(20):
        for j in range(20):
            a = random_slope[i][j]
            x, y = line(i, j, a)
            z = np.full_like(x, (height+1)*thickness+1)
            seg = gc.Path(x, y, z)
            full_object.append(seg)


gc.gui_export(full_object)