import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import copy
import sys
import configparser
import math

ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' # 追加
CONFIG_PATH = ROUTE_PATH + '/print_setting.ini' # 編集
print_setting = configparser.ConfigParser()
print_setting.read(CONFIG_PATH)
KINEMATICS = print_setting['Kinematics']['Kinematics']
DEGREE_DIVIDE = 18.0

pos_array = []
noz_array = []
idx_array = []

def vecA_to_vecB(a, b):
    cross = np.zeros(3)
    cross[0] = a[1]*b[2] - a[2]*b[1]
    cross[1] = a[2]*b[0] - a[0]*b[2]
    cross[2] = a[0]*b[1] - a[1]*b[0]
    norm = math.sqrt(cross[0]*cross[0] + cross[1]*cross[1] + cross[2]*cross[2])
    cross[0] /= norm
    cross[1] /= norm
    cross[2] /= norm
    dot = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
    ang = math.acos(dot)
    return (cross, ang)

def set_object_array(full_object):
    global pos_array, noz_array, idx_array
    if KINEMATICS == 'Cartesian':
        pos_array = copy.deepcopy(full_object)
        for layer_list in pos_array:
            sub_noz_array = []
            for segment in layer_list:
                if len(segment) > 3:
                    del segment[3:]
                sub_noz_array.append((0,0))
            noz_array.append(sub_noz_array)
    elif KINEMATICS == 'BedTiltBC':
        pos_array = []
        noz_array = []
        idx_array = []
        px = full_object[0][0][0]
        py = full_object[0][0][1]
        pz = full_object[0][0][2]
        ptilt = full_object[0][0][3]
        prot = full_object[0][0][4]
        for layer_list in full_object:
            layer_pos_array = []
            layer_noz_array = []
            sub_idx_array = []
            for segment in layer_list:
                x = segment[0]
                y = segment[1]
                z = segment[2]
                tilt = segment[3]
                rot = segment[4]
                div1 = math.ceil( (tilt - ptilt) / (math.pi / DEGREE_DIVIDE) )
                div2 = math.ceil( (rot - prot) / (math.pi / DEGREE_DIVIDE) )
                div = max(1, div1, div2)
                for i in range(div):
                    #print('loop_c')
                    btilt = (tilt - ptilt) / div * i + ptilt
                    brot = (rot - prot) / div * i + prot
                    bx1 = (x - px) / div * i + px
                    by1 = (y - py) / div * i + py
                    bz1 = (z - pz) / div * i + pz
                    bx2 = bx1 * math.cos(btilt) - bz1 * math.sin(btilt)
                    by2 = by1
                    bz2 = bx1 * math.sin(btilt) + bz1 * math.cos(btilt)
                    bx3 = bx2 * math.cos(-brot) - by2 * math.sin(-brot)
                    by3 = bx2 * math.sin(-brot) + by2 * math.cos(-brot)
                    bz3 = bz2
                    pos = (bx3, by3, bz3)
                    noz = (btilt, brot)
                    layer_pos_array.append(pos)
                    layer_noz_array.append(noz)
                px = x
                py = y
                pz = z
                ptilt = tilt
                prot = rot
                sub_idx_array.append(len(layer_pos_array))
            idx_array.append(sub_idx_array)
            if len(layer_pos_array) > 0:
                pos_array.append(layer_pos_array)
                noz_array.append(layer_noz_array)
    elif KINEMATICS == 'NozzleTilt':
        pos_array = copy.deepcopy(full_object)
        for layer_list in pos_array:
            sub_noz_array = []
            for segment in layer_list:
                sub_noz_array.append((segment[3:5]))
                if len(segment) > 3:
                    del segment[3:]
            noz_array.append(sub_noz_array)

def draw_object_array(widget,slider_layer, slider_segment):
    #global pos_array, noz_array
    buf_array = []
    for i in range(slider_layer - 1):
        buf_array.append(pos_array[i])
    buf_array.append(pos_array[slider_layer - 1][:slider_segment - 1])
    
    for i in range(len(buf_array)):
        if len(buf_array[i]) > 1:
            plt = gl.GLLinePlotItem(pos = buf_array[i] ,color = pg.intColor(i,len(pos_array),alpha=180),width=0.5, antialias = True)
            widget.addItem(plt) 

    mesh = gl.MeshData.cylinder(rows = 8, cols = 8, radius = [1.0, 5.0], length = 10.0)
    plt = gl.GLMeshItem(meshdata = mesh)
    if KINEMATICS == 'Cartesian':
        pos_x = pos_array[slider_layer-1][slider_segment-1][0]
        pos_y = pos_array[slider_layer-1][slider_segment-1][1]
        pos_z = pos_array[slider_layer-1][slider_segment-1][2]
        plt.translate(pos_x, pos_y, pos_z)
        widget.addItem(plt)
    elif KINEMATICS == 'BedTiltBC':
        pos_x = pos_array[slider_layer-1][ idx_array[slider_layer-1][slider_segment-1]-1 ][0]
        pos_y = pos_array[slider_layer-1][ idx_array[slider_layer-1][slider_segment-1]-1 ][1]
        pos_z = pos_array[slider_layer-1][ idx_array[slider_layer-1][slider_segment-1]-1 ][2]
        tilt = noz_array[slider_layer-1][ idx_array[slider_layer-1][slider_segment-1]-1 ][0]
        rot = noz_array[slider_layer-1][ idx_array[slider_layer-1][slider_segment-1]-1 ][1]
        rot = rot + math.pi
        mat = ( (math.cos(rot) * math.cos(tilt), math.sin(rot), math.cos(rot) * math.sin(tilt)),
                (-math.sin(rot) * math.cos(tilt), math.cos(rot), -math.sin(rot) * math.sin(tilt)),
                (-math.sin(tilt), 0, math.cos(tilt)) )
        norm = (mat[0][2], mat[1][2], mat[2][2])
        (cross, ang) = vecA_to_vecB((0,0,1), (norm[0],norm[1],norm[2]))
        plt.rotate(math.degrees(ang), cross[0], cross[1], cross[2])
        plt.translate(pos_x, pos_y, pos_z)
        widget.addItem(plt)
    elif KINEMATICS == 'NozzleTilt':
        pos_x = pos_array[slider_layer-1][slider_segment-1][0]
        pos_y = pos_array[slider_layer-1][slider_segment-1][1]
        pos_z = pos_array[slider_layer-1][slider_segment-1][2]
        tilt = noz_array[slider_layer-1][slider_segment-1][0]
        rot = noz_array[slider_layer-1][slider_segment-1][1]
        rot = -rot + math.pi / 2.0
        mat = ( (math.cos(rot), math.sin(rot) * math.cos(tilt), math.sin(rot) * math.sin(tilt)),
                (-math.sin(rot), math.cos(rot) * math.cos(tilt), math.cos(rot) * math.sin(tilt)),
                (0, -math.sin(tilt), math.cos(tilt)))
        norm = (mat[0][2], mat[1][2], mat[2][2])
        (cross, ang) = vecA_to_vecB((0,0,1), (norm[0],norm[1],norm[2]))
        plt.rotate(math.degrees(ang), cross[0], cross[1], cross[2])
        plt.translate(pos_x, pos_y, pos_z)
        widget.addItem(plt)
        
        