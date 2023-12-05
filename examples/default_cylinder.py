import math
import numpy as np
import gcoordinator as gc
import time
from tqdm import tqdm

LAYER = 100

full_object=[]
for height in tqdm(range(LAYER)):
    arg = np.linspace(0, 2*np.pi, 100)
    x = 10 * np.cos(arg)
    y = 10 * np.sin(arg)
    z = np.full_like(arg, (height+1) * 0.2)
    wall = gc.Path(x, y, z)
    full_object.append(wall)
    #print(f'layer {height}')
    time.sleep(0.01)
gc.gui_export(full_object)