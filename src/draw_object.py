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


pos_array = []
noz_array = []
idx_array = []


def set_object_array(full_object):
    global pos_array, noz_array, idx_array
    pos_array = copy.deepcopy(full_object)
    for layer_list in pos_array:
        sub_noz_array = []
        for segment in layer_list:
            if len(segment) > 3:
                del segment[3:]
            sub_noz_array.append((0,0))
        noz_array.append(sub_noz_array)
    

def draw_object_array(widget,slider_layer, slider_segment):
    #global pos_array, noz_array
    buf_array = []
    for i in range(slider_layer - 1):
        buf_array.append(pos_array[i])
    buf_array.append(pos_array[slider_layer - 1][:slider_segment - 1])
    
    for i in range(len(buf_array)):
        if len(buf_array[i]) > 1:
            plt = gl.GLLinePlotItem(pos = buf_array[i] ,color = pg.intColor(pos_array[i][0][2],300,alpha=80),width=0.5, antialias = True)
            widget.addItem(plt) 

    mesh = gl.MeshData.cylinder(rows = 8, cols = 8, radius = [1.0, 5.0], length = 10.0)
    plt = gl.GLMeshItem(meshdata = mesh, smooth=True, color=(1.0, 1.0, 1.0, 0.7), shader='shaded')
    plt.setGLOptions('translucent')
    
    pos_x = pos_array[slider_layer-1][slider_segment-1][0]
    pos_y = pos_array[slider_layer-1][slider_segment-1][1]
    pos_z = pos_array[slider_layer-1][slider_segment-1][2]
    plt.translate(pos_x, pos_y, pos_z)
    widget.addItem(plt)
    