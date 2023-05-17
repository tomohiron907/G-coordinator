import numpy as np
import math
import print_settings
from kinematics.kin_base import *

class NozzleTilt(Kinematics):
    def __init__(self, machine_settings):
        self.axes_count = 5
        self.tilt_code = machine_settings['Kinematics']['nozzletilt.tilt_code']
        self.rot_code = machine_settings['Kinematics']['nozzletilt.rot_code']
        self.tilt_offset = float(machine_settings['Kinematics']['nozzletilt.tilt_offset'])
        self.rot_offset = float(machine_settings['Kinematics']['nozzletilt.rot_offset'])
        

        
    def e_calc(self, path):
        path.Eval = np.array([0])
        for i in range(len(path.coords)-1):
            Dis = math.sqrt((path.x[i+1]-path.x[i])**2 + (path.y[i+1]-path.y[i])**2 + (path.z[i+1]-path.z[i])**2)
            AREA=(print_settings.nozzle_diameter-print_settings.layer_height)*(print_settings.layer_height)+(print_settings.layer_height/2)**2*np.pi
            path.Eval = np.append(path.Eval, 4*AREA*Dis/(np.pi*print_settings.filament_diameter**2))
        
    def coords_arrange(self, path):
        path.coords = np.column_stack([path.x, path.y, path.z])
        path.norms = []
        for (rot,tilt) in zip(path.rot,path.tilt):
            rot = -rot +math.pi / 2.0
            mat = ( (math.cos(rot), math.sin(rot) * math.cos(tilt), math.sin(rot) * math.sin(tilt)),
                    (-math.sin(rot), math.cos(rot) * math.cos(tilt), math.cos(rot) * math.sin(tilt)),
                    (0, -math.sin(tilt), math.cos(tilt)))
            norm = (mat[0][2], mat[1][2], mat[2][2])
            path.norms.append(norm)        
        
        path.center = np.array([np.mean(path.x), np.mean(path.y), np.mean(path.z)])
        path.start_coord = path.coords[0]
        path.end_coord = path.coords[-1]
        path.center = np.array([np.mean(path.x), np.mean(path.y), np.mean(path.z)])
        path.start_coord = path.coords[0]
        path.end_coord = path.coords[-1]
        return path.coords, path.norms