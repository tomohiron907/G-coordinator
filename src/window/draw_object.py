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
import colorsys
import time

ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' # 追加
CONFIG_PATH = ROUTE_PATH + '/settings/print_setting.ini' # 編集
print_setting = configparser.ConfigParser()
print_setting.read(CONFIG_PATH)

def vecA_to_vecB(a, b):
    """Calculation of direction and angle of nozzle drawing direction

    Args:
        a (tuple): original normal vector
        b (tuple): normal vector

    Returns:
        tuple: direction and angle of nozzle drawing direction
    """
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



def draw_full_object(widget, full_object):
    """Create and draw a sequence of coordinates that the nozzle moves through the entire list of full_objects

    Args:
        widget (GLViewWidget): widget of graphics view
        full_object (list): list of path objects
    """
    global pos_array,colors
    pos_array = []
    colors = []
    for idx, path in enumerate(full_object):
        coord = path.coords
        norms = path.norms
        color = np.zeros((len(coord), 4))
        for i in range(len(coord)):
            z = coord[i][2]
            hue = z % 360  
            rgb = colorsys.hsv_to_rgb(hue/360, 1, 1)  
            color[i] = (*rgb, 1)  

        coord = np.insert(coord, 1, coord[0], axis=0)
        coord = np.append(coord, [coord[-1]], axis=0)
        
        color = np.insert(color, 0, (1, 1, 1, 0.1), axis=0)
        color = np.append(color, [(1, 1, 1, 0.1)], axis=0)
        
        pos_array.append(coord)
        colors.append(color)
    
    pos_array = np.concatenate(pos_array)
    colors = np.concatenate(colors)

    plt = gl.GLLinePlotItem(pos=pos_array, color=colors, width=0.5, antialias=True)
    
    widget.addItem(plt)
    slider_layer = len(full_object)-1
    slider_segment = len(full_object[-1].coords)
    current_path = full_object[slider_layer]
    current_path_plot_coords = current_path.coords[:slider_segment]
    plt_last = gl.GLLinePlotItem(pos= current_path_plot_coords, color = 'w', width = 1, antialias = True)
    widget.addItem(plt_last)
    norm = current_path.norms[slider_segment - 1]
    
    if slider_layer > 0 and slider_segment > 0:
        mesh = gl.MeshData.cylinder(rows=8, cols=8, radius=[1.0, 5.0], length=10.0)
        plt = gl.GLMeshItem(meshdata=mesh, smooth=True, color=(1.0, 1.0, 1.0, 0.5), shader='shaded')
        plt.setGLOptions('translucent')
        pos_x = current_path_plot_coords[-1][0]
        pos_y = current_path_plot_coords[-1][1]
        pos_z = current_path_plot_coords[-1][2]
        (cross, ang) = vecA_to_vecB((0, 0, 1), norm)
        plt.rotate(math.degrees(ang), cross[0], cross[1], cross[2])
        plt.translate(pos_x, pos_y, pos_z)
        widget.addItem(plt)



def draw_object_slider(widget, full_object, slider_layer, slider_segment):
    """Calculates how many segments to draw from the slider value and sets subsequent segments as transparent

    Args:
        widget (GLViewWidget): widget of graphics view
        full_object (list): list of path objects
        slider_layer (int): slider_layer value
        slider_segment (int): segment_layer value
    """
    global pos_array, colors
    colors_copy = np.copy(colors)
    segment_each_path = 0
    for idx, path in enumerate(full_object):
        
        if idx < slider_layer :
            segment_each_path += len((full_object[idx].coords))
            segment_each_path += 2
    segment_each_path += slider_segment
    colors_copy[segment_each_path:, 3] = 0.0
    plt = gl.GLLinePlotItem(pos=pos_array, color=colors_copy, width=0.5, antialias=True)
    
    widget.addItem(plt)
    current_path = full_object[slider_layer]
    current_path_plot_coords = current_path.coords[:slider_segment]
    plt_last = gl.GLLinePlotItem(pos= current_path_plot_coords, color = 'w', width = 1, antialias = True)
    widget.addItem(plt_last)
    norm = current_path.norms[slider_segment - 1]
    
    if slider_layer > 0 and slider_segment > 0:
        mesh = gl.MeshData.cylinder(rows=8, cols=8, radius=[1.0, 5.0], length=10.0)
        plt = gl.GLMeshItem(meshdata=mesh, smooth=True, color=(1.0, 1.0, 1.0, 0.5), shader='shaded')
        plt.setGLOptions('translucent')
        pos_x = current_path_plot_coords[-1][0]
        pos_y = current_path_plot_coords[-1][1]
        pos_z = current_path_plot_coords[-1][2]
        (cross, ang) = vecA_to_vecB((0, 0, 1), norm)
        plt.rotate(math.degrees(ang), cross[0], cross[1], cross[2])
        plt.translate(pos_x, pos_y, pos_z)
        widget.addItem(plt)


