import numpy as np
import math
import print_settings
from kinematics.kin_base import *
PRE_MOVE_DIV = 10

class BedRotate(Kinematics):
    def __init__(self, print_setting):
        self.axes_count = 4
        self.rot_code = print_setting['kinematics']['rot_code']
        self.rot_offset = float(print_setting['kinematics']['rot_offset'])
        self.div_distance = float(print_setting['kinematics']['div_distance'])
        
    def add_parameter_tree(self):
        param = {'name': 'kinematics', 'type': 'group', 'children': [
            {'name': 'kin_name', 'type': 'str', 'value': 'BedRotate'},
            {'name': 'rot_name', 'type': 'str', 'value': self.rot_code},
            {'name': 'rot_offset', 'type': 'float', 'value': self.rot_offset},
            {'name': 'div_distance', 'type': 'float', 'value': self.div_distance},
        ]},
        return param
        
    def e_calc(self, path):
        path.Eval = np.array([0])
        px = path.coords[0][0]
        py = path.coords[0][1]
        pz = path.coords[0][2]
        idx = 0
        for i in range(len(path.x[1:])):
            Dis = 0.0
            for j in range(path.sub_segment_cnt[i]):
                idx += 1
                nx = path.coords[idx][0]
                ny = path.coords[idx][1]
                nz = path.coords[idx][2]
                Dis += math.sqrt((nx-px)**2 + (ny-py)**2 + (nz-pz)**2)
                px = nx
                py = ny
                pz = nz
            AREA=(print_settings.nozzle_diameter-print_settings.layer_height)*(print_settings.layer_height)+(print_settings.layer_height/2)**2*np.pi
            path.Eval = np.append(path.Eval, 4*AREA*Dis/(np.pi*print_settings.filament_diameter**2))        
        
    def coords_arrange(self, path):
        coords = []
        norms = []
        path.sub_segment_cnt = []
        ppx = px = path.x[0]
        ppy = py = path.y[0]
        ppz = pz = path.z[0]
        pprot = prot = path.rot[0]
        # start pos
        bx2 = px * math.cos(-prot) - py * math.sin(-prot)
        by2 = px * math.sin(-prot) + py * math.cos(-prot)
        bz2 = pz
        pos = (bx2, by2, bz2)
        coords.append(pos)
        for (nx,ny,nz,nrot) in zip(path.x[1:],path.y[1:],path.z[1:],path.rot[1:]):
            # pre calc
            Dis = 0.0
            for i in range(PRE_MOVE_DIV):
                bx1 = (nx - px) * (i+1) / PRE_MOVE_DIV + px
                by1 = (ny - py) * (i+1) / PRE_MOVE_DIV + py
                bz1 = (nz - pz) * (i+1) / PRE_MOVE_DIV + pz
                brot = (nrot - prot) * (i+1) / PRE_MOVE_DIV + prot
                # calc pos
                bx2 = bx1 * math.cos(-brot) - by1 * math.sin(-brot)
                by2 = bx1 * math.sin(-brot) + by1 * math.cos(-brot)
                bz2 = bz1
                # distance
                Dis += math.sqrt((bx2-ppx)**2 + (by2-ppy)**2 + (bz2-ppz)**2)
                # sub prev
                ppx = bx2
                ppy = by2
                ppz = bz2
                pprot = brot
            # calc coords
            div = (int)(np.ceil(Dis / self.div_distance))
            path.sub_segment_cnt.append(div)
            for i in range(div):
                bx1 = (nx - px) * (i+1) / div + px
                by1 = (ny - py) * (i+1) / div + py
                bz1 = (nz - pz) * (i+1) / div + pz
                brot = (nrot - prot) * (i+1) / div + prot
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
            
        center_x = center_y = center_z = 0.0
        for coord in coords:
            center_x += coord[0]
            center_y += coord[1]
            center_z += coord[2]
        center_x /= len(coords)
        center_y /= len(coords)
        center_z /= len(coords)
        path.coords = coords
        path.norms = norms
        path.center = (center_x, center_y, center_z)
        path.start_coord = path.coords[0]
        path.end_coord = path.coords[-1]
        return path.coords, path.norms