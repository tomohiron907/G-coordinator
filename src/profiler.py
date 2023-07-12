from line_profiler import LineProfiler
from draw_object import profile_for
import numpy as np
import print_settings 
from path_generator import *


LAYER = 100
profiler = LineProfiler()
profiler.add_function(profile_for)

full_object=[]
for height in range(LAYER):
    arg = np.linspace(0, 2*np.pi, 100)
    x = 10 * np.cos(arg)
    y = 10 * np.sin(arg)
    z = np.full_like(arg, (height+1) * print_settings.layer_height)
    wall = Path(x, y, z)
    full_object.append(wall)




profiler.runctx('profile_for(full_object)', globals(), locals())
profiler.print_stats()


#kernprof -l -v profiler.py