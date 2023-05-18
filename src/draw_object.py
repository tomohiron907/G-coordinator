import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import copy
import sys
import configparser
import math
from print_settings import *
from kinematics.kin_base import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

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



def draw_object_array(widget, full_object, slider_layer, slider_segment):
    # 3回メソッドが呼び出されてるのを修正？
    pos_array = []
    colors = []
    '''for idx, path in enumerate(full_object):
        #coords = path.coords
        norms = path.norms
        if idx == slider_layer - 1:
            pos_array.append(coords[:slider_segment])
            norm = norms[slider_segment - 1]
        elif idx < slider_layer - 1:
            pos_array.append(coords)
            norm = norms[-1]
        if len(coords) > 0:
            z = coords[0][2]
            r = int(255 * (1 - z / 200))
            g = int(255 * (z / 200))
            color = QColor(r, g, 0, 100)
            vertex_colors = [color.getRgbF()] * (len(coords))
            colors.extend(vertex_colors)'''

    for idx, path in enumerate(full_object):
        coord = path.coords
        norms = path.norms
        #norm = norms[slider_segment - 1]
        norm = (0, 0, 1)
        if idx < slider_layer-1:
            color = np.zeros((len(coord), 4))
            for i in range(len(coord)):
                z = coord[i][2]
                r = ((1 - z / 100))
                g = ((z / 100))
                b = z/100
                color[i] = (r, g, b, 1)

            coord = np.insert(coord, 1, coord[0], axis = 0)
            coord = np.append(coord, [coord[-1]], axis = 0)
            color = np.insert(color, 0, (1, 1, 1, 0.1), axis = 0)
            color = np.append(color, [(1, 1, 1, 0.1)], axis = 0)
            pos_array.extend(coord)
            colors.extend(color)
        elif idx == slider_layer:
            pos_array.extend(coord[:slider_segment])
            color = np.ones((slider_segment, 4))
            colors.extend(color)
    #pos_array = np.concatenate(pos_array, axis=0)
    pos_array = np.array(pos_array)
    colors = np.array(colors)
    #print(f'{pos_array=}')
    #print(f'{colors=}')
    #print(colors)
    plt = gl.GLLinePlotItem(pos=pos_array, color=colors, width=0.5, antialias=True)
    widget.addItem(plt)

    if slider_layer > 1 and slider_segment > 0:
        mesh = gl.MeshData.cylinder(rows=8, cols=8, radius=[1.0, 5.0], length=10.0)
        plt = gl.GLMeshItem(meshdata=mesh, smooth=True, color=(1.0, 1.0, 1.0, 0.5), shader='shaded')
        plt.setGLOptions('translucent')
        pos_x = pos_array[-1][0]
        pos_y = pos_array[-1][1]
        pos_z = pos_array[-1][2]
        (cross, ang) = vecA_to_vecB((0, 0, 1), norm)
        plt.rotate(math.degrees(ang), cross[0], cross[1], cross[2])
        plt.translate(pos_x, pos_y, pos_z)
        widget.addItem(plt)

def qcolor_to_rgb(qcolor):
    r = qcolor.red()
    g = qcolor.green()
    b = qcolor.blue()
    return [r, g, b]
    