import numpy as np
import math
import print_settings
from kinematics.kin_base import *
MOVE_DIV = 10

class BedTiltBC(Kinematics):
    def __init__(self, print_setting):
        self.axes_count = 5
        self.tilt_code = print_setting['kinematics']['tilt_code']
        self.rot_code = print_setting['kinematics']['rot_code']
        self.tilt_offset = float(print_setting['kinematics']['tilt_offset'])
        self.rot_offset = float(print_setting['kinematics']['rot_offset'])
        
    def add_parameter_tree(self):
        param = {'name': 'kinematics', 'type': 'group', 'children': [
            {'name': 'kin_name', 'type': 'str', 'value': 'BedTiltBC'},
            {'name': 'tilt_code', 'type': 'str', 'value': self.tilt_code},
            {'name': 'rot_name', 'type': 'str', 'value': self.rot_code},
            {'name': 'tilt_offset', 'type': 'float', 'value': self.tilt_offset},
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
        ptilt = path.tilt[0]
        for (nx,ny,nz,nrot,ntilt) in zip(path.x[1:],path.y[1:],path.z[1:],path.rot[1:],path.tilt[1:]):
            for i in range(MOVE_DIV+1):
                bx1 = (nx - px) * i / MOVE_DIV + px
                by1 = (ny - py) * i / MOVE_DIV + py
                bz1 = (nz - pz) * i / MOVE_DIV + pz
                brot = (nrot - prot) * i / MOVE_DIV + prot
                btilt = (ntilt - ptilt) * i / MOVE_DIV + ptilt
                # calc pos
                bx2 = bx1 * math.cos(btilt) - bz1 * math.sin(btilt)
                by2 = by1
                bz2 = bx1 * math.sin(btilt) + bz1 * math.cos(btilt)
                bx3 = bx2 * math.cos(-brot) - by2 * math.sin(-brot)
                by3 = bx2 * math.sin(-brot) + by2 * math.cos(-brot)
                bz3 = bz2
                # distance
                Dis += math.sqrt((bx3-px)**2 + (by3-py)**2 + (bz3-pz)**2)
            # prev
            px = bx3
            py = by3
            pz = bz3
            prot = brot
            ptilt = btilt
            AREA=(print_settings.nozzle_diameter-print_settings.layer_height)*(print_settings.layer_height)+(print_settings.layer_height/2)**2*np.pi
            path.Eval = np.append(path.Eval, 4*AREA*Dis/(np.pi*print_settings.filament_diameter**2))            
        
    def coords_arrange(self, path):
        coords = []
        norms = []
        px = path.x[0]
        py = path.y[0]
        pz = path.z[0]
        prot = path.rot[0]
        ptilt = path.tilt[0]
        for (nx,ny,nz,nrot,ntilt) in zip(path.x[1:],path.y[1:],path.z[1:],path.rot[1:],path.tilt[1:]):
            for i in range(MOVE_DIV+1):
                bx1 = (nx - px) * i / MOVE_DIV + px
                by1 = (ny - py) * i / MOVE_DIV + py
                bz1 = (nz - pz) * i / MOVE_DIV + pz
                brot = (nrot - prot) * i / MOVE_DIV + prot
                btilt = (ntilt - ptilt) * i / MOVE_DIV + ptilt
                # calc pos
                bx2 = bx1 * math.cos(btilt) - bz1 * math.sin(btilt)
                by2 = by1
                bz2 = bx1 * math.sin(btilt) + bz1 * math.cos(btilt)
                bx3 = bx2 * math.cos(-brot) - by2 * math.sin(-brot)
                by3 = bx2 * math.sin(-brot) + by2 * math.cos(-brot)
                bz3 = bz2
                pos = (bx3, by3, bz3)
                coords.append(pos)
                # calc norm
                mat = ( (math.cos(brot) * math.cos(-btilt), math.sin(brot), math.cos(brot) * math.sin(-btilt)),
                        (-math.sin(brot) * math.cos(-btilt), math.cos(brot), -math.sin(brot) * math.sin(-btilt)),
                        (-math.sin(-btilt), 0, math.cos(-btilt)) )
                norm = (mat[0][2], mat[1][2], mat[2][2])
                norms.append(norm)
            # prev
            px = bx3
            py = by3
            pz = bz3
            prot = brot
            ptilt = btilt
        path.coords = coords
        path.norms = norms
        path.center = np.array([np.mean(path.x), np.mean(path.y), np.mean(path.z)])
        path.start_coord = path.coords[0]
        path.end_coord = path.coords[-1]
        return path.coords, path.norms