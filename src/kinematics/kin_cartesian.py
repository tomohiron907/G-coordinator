import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import copy
import sys

import numpy as np
import math
from kinematics.kin_base import *
        
class Cartesian(Kinematics):
    def __init__(self, print_setting):
        super().__init__(print_setting)
        self.axes_count = 3
        
    def add_parameter_tree(self):
        param = {'name': 'Kinematics', 'type': 'group', 'children': [
            {'name': 'Name', 'type': 'str', 'value': 'Cartesian'},
        ]},
        return param
        
    def e_calc(self, path):
        path.Eval = np.array([0])
        for i in range(len(path.coords)-1):
            Dis = math.sqrt((path.x[i+1]-path.x[i])**2 + (path.y[i+1]-path.y[i])**2 + (path.z[i+1]-path.z[i])**2)
            AREA=(self.NOZZLE-self.LAYER)*(self.LAYER)+(self.LAYER/2)**2*np.pi
            path.Eval = np.append(path.Eval, 4*AREA*Dis/(np.pi*self.FILAMENT_DIAMETER**2))

    def draw_object_array(self, widget,full_object,slider_layer, slider_segment):
        #global pos_array, noz_array
        pos_array = []
        for path in full_object:
            pos_array.append(path.coords)
        buf_array = []
        for i in range(slider_layer - 1):
            buf_array.append(pos_array[i])
        buf_array.append(pos_array[slider_layer - 1][:slider_segment ])
        if slider_layer == 0:
            buf_array = []
        
        if slider_layer==len(pos_array):
            for i in range(slider_layer):
                if len(pos_array[i])==1:
                    continue
                else:
                    plt = gl.GLLinePlotItem(pos = buf_array[i] ,color = pg.intColor(pos_array[i][0][2],300,alpha=180),width=0.5, antialias = True)
                    widget.addItem(plt)
        
        else:
            for i in range(len(buf_array)):
                if i == slider_layer-1: # current layer display
                    if slider_segment > 1:
                        plt = gl.GLLinePlotItem(pos = buf_array[i] ,color = pg.mkColor('w'),width=0.8, antialias = True)
                        widget.addItem(plt)
                    else:
                        pass
                else:
                    if len(buf_array[i]) > 1:
                        plt = gl.GLLinePlotItem(pos = buf_array[i] ,color = pg.intColor(pos_array[i][0][2],300,alpha=180),width=0.5, antialias = True)
                        widget.addItem(plt) 

        if slider_layer > 1 and slider_segment > 0:
            #print(slider_segment)
            mesh = gl.MeshData.cylinder(rows = 8, cols = 8, radius = [1.0, 5.0], length = 10.0)
            plt = gl.GLMeshItem(meshdata = mesh, smooth=True, color=(1.0, 1.0, 1.0, 0.5), shader='shaded')
            plt.setGLOptions('translucent')
            pos_x = buf_array[slider_layer-1][slider_segment-1][0]
            pos_y = buf_array[slider_layer-1][slider_segment-1][1]
            pos_z = buf_array[slider_layer-1][slider_segment-1][2]
            plt.translate(pos_x, pos_y, pos_z)
            widget.addItem(plt)