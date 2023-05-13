import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import copy
import sys
import configparser
import math
from print_settings import *
from kinematics.kin_base import *

ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' # 追加
CONFIG_PATH = ROUTE_PATH + '/print_setting.ini' # 編集
print_setting = configparser.ConfigParser()
print_setting.read(CONFIG_PATH)

def vecA_to_vecB(a, b):
    cross = np.zeros(3)
    cross[0] = a[1]*b[2] - a[2]*b[1]
    cross[1] = a[2]*b[0] - a[0]*b[2]
    cross[2] = a[0]*b[1] - a[1]*b[0]
    norm = math.sqrt(cross[0]*cross[0] + cross[1]*cross[1] + cross[2]*cross[2])
    if norm == 0.0:
        cross[0] = 0.0
        cross[1] = 0.0
        cross[2] = 1.0
        ang = 0.0
    else:
        cross[0] /= norm
        cross[1] /= norm
        cross[2] /= norm
        dot = a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
        ang = math.acos(dot)
    return (cross, ang)

def draw_object_array(widget,full_object,slider_layer, slider_segment):
    pos_array = []
    for idx, path in enumerate(full_object):
        coords = path.coords
        norms = path.norms
        if idx == slider_layer - 1:
            pos_array.append(coords[:slider_segment])
            norm = norms[slider_segment-1]
        elif idx < slider_layer - 1:
            pos_array.append(coords)
            norm = norms[-1]
    
    if slider_layer==len(pos_array):
        for i in range(slider_layer):
            if len(pos_array[i]) > 1:
                plt = gl.GLLinePlotItem(pos = pos_array[i] ,color = pg.intColor(pos_array[i][0][2],300,alpha=180),width=0.5, antialias = True)
                widget.addItem(plt)
    
    else:
        for i in range(len(pos_array)):
            if i == slider_layer-1: # current layer display
                if slider_segment > 0:
                    plt = gl.GLLinePlotItem(pos = pos_array[i] ,color = pg.mkColor('w'),width=0.8, antialias = True)
                    widget.addItem(plt)
                else:
                    pass
            else:
                if len(pos_array[i]) > 0:
                    plt = gl.GLLinePlotItem(pos = pos_array[i] ,color = pg.intColor(pos_array[i][0][2],300,alpha=180),width=0.5, antialias = True)
                    widget.addItem(plt) 

    if slider_layer > 1 and slider_segment > 0:
        mesh = gl.MeshData.cylinder(rows = 8, cols = 8, radius = [1.0, 5.0], length = 10.0)
        plt = gl.GLMeshItem(meshdata = mesh, smooth=True, color=(1.0, 1.0, 1.0, 0.5), shader='shaded')
        plt.setGLOptions('translucent')
        pos_x = pos_array[-1][-1][0]
        pos_y = pos_array[-1][-1][1]
        pos_z = pos_array[-1][-1][2]
        (cross, ang) = vecA_to_vecB((0, 0, 1), norm)
        plt.rotate(math.degrees(ang), cross[0], cross[1], cross[2])
        plt.translate(pos_x, pos_y, pos_z)
        widget.addItem(plt)
    