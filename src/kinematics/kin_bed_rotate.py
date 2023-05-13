import numpy as np
import math
import print_settings
from kinematics.kin_base import *
MOVE_DIV = 10

class BedRotate(Kinematics):
    def __init__(self, print_setting):
        self.axes_count = 4
        self.rot_code = print_setting['kinematics']['rot_code']
        self.rot_offset = float(print_setting['kinematics']['rot_offset'])
        
    def add_parameter_tree(self):
        param = {'name': 'kinematics', 'type': 'group', 'children': [
            {'name': 'kin_name', 'type': 'str', 'value': 'BedRotate'},
            {'name': 'rot_name', 'type': 'str', 'value': self.rot_code},
            {'name': 'rot_offset', 'type': 'float', 'value': self.rot_offset},
        ]},
        return param
        
    def e_calc(self, path):
        path.Eval = np.array([0])
        Dis = 0.0
        px = path.x[0]
        py = path.y[0]
        pz = path.z[0]
        prot = path.rot[0]
        for (nx,ny,nz,nrot) in zip(path.x[1:],path.y[1:],path.z[1:],path.rot[1:]):
            for i in range(MOVE_DIV+1):
                bx1 = (nx - px) * i / MOVE_DIV + px
                by1 = (ny - py) * i / MOVE_DIV + py
                bz1 = (nz - pz) * i / MOVE_DIV + pz
                brot = (nrot - prot) * i / MOVE_DIV + prot
                # calc pos
                bx2 = bx1 * math.cos(-brot) - by1 * math.sin(-brot)
                by2 = bx1 * math.sin(-brot) + by1 * math.cos(-brot)
                bz2 = bz1
                # distance
                Dis += math.sqrt((bx2-px)**2 + (by2-py)**2 + (bz2-pz)**2)
            # prev
            px = bx2
            py = by2
            pz = bz2
            prot = brot
            AREA=(print_settings.nozzle_diameter-print_settings.layer_height)*(print_settings.layer_height)+(print_settings.layer_height/2)**2*np.pi
            path.Eval = np.append(path.Eval, 4*AREA*Dis/(np.pi*print_settings.filament_diameter**2))            
        
    def coords_arrange(self, path):
        coords = []
        norms = []
        px = path.x[0]
        py = path.y[0]
        pz = path.z[0]
        prot = path.rot[0]
        for (nx,ny,nz,nrot) in zip(path.x[1:],path.y[1:],path.z[1:],path.rot[1:]):
            for i in range(MOVE_DIV+1):
                bx1 = (nx - px) * i / MOVE_DIV + px
                by1 = (ny - py) * i / MOVE_DIV + py
                bz1 = (nz - pz) * i / MOVE_DIV + pz
                brot = (nrot - prot) * i / MOVE_DIV + prot
                # calc pos
                bx2 = bx1 * math.cos(-brot) - by1 * math.sin(-brot)
                by2 = bx1 * math.sin(-brot) + by1 * math.cos(-brot)
                bz2 = bz1
                pos = (bx2, by2, bz2)
                coords.append(pos)
            # prev
            px = bx2
            py = by2
            pz = bz2
            prot = brot
        for i in range(len(coords)):
            norms.append((0, 0, 1))
        
        path.coords = coords
        path.norms = norms
        path.center = np.array([np.mean(path.x), np.mean(path.y), np.mean(path.z)])
        path.start_coord = path.coords[0]
        path.end_coord = path.coords[-1]
        return path.coords, path.norms