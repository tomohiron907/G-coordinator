import numpy as np
import math
import print_settings
from kinematics.kin_base import *

class Cartesian(Kinematics):
    def __init__(self, print_setting):
        self.axes_count = 3
        
    def add_parameter_tree(self):
        return None
        
    def e_calc(self, path):
        path.Eval = np.array([0])
        for i in range(len(path.x)-1):
            Dis = math.sqrt((path.x[i+1]-path.x[i])**2 + (path.y[i+1]-path.y[i])**2 + (path.z[i+1]-path.z[i])**2)
            AREA=(print_settings.nozzle_diameter-print_settings.layer_height)*(print_settings.layer_height)+(print_settings.layer_height/2)**2*np.pi
            path.Eval = np.append(path.Eval, 4*AREA*Dis/(np.pi*print_settings.filament_diameter**2))
        
    def coords_arrange(self, path):
        path.coords = np.column_stack([path.x, path.y, path.z])
        path.center = np.array([np.mean(path.x), np.mean(path.y), np.mean(path.z)])
        path.start_coord = path.coords[0]
        path.end_coord = path.coords[-1]
        norms = []
        for i in range(len(path.coords)):
            norms.append((0, 0, 1))
        path.norms = norms
        return path.coords, path.norms