import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import copy



def draw_object_array(full_object,widget,slider):
    pos_array = copy.deepcopy(full_object)
    for layer_list in pos_array:
        for segment in layer_list:
            if len(segment) == 5 or len(segment)==4:
                del segment[3:]
            else:
                pass

    if slider==len(pos_array):
        for i in range(slider):
            if len(pos_array[i])==1:
                continue
            else:
                plt = gl.GLLinePlotItem(pos = pos_array[i] ,color = pg.intColor(pos_array[i][0][2],300,alpha=180),width=0.5, antialias = True)
                widget.addItem(plt)
    
    else:
        for i in range(slider):
            if i == slider-1:
                plt = gl.GLLinePlotItem(pos = pos_array[i] ,color = pg.mkColor('w'),width=0.8, antialias = True)
                widget.addItem(plt)
            else:
                plt = gl.GLLinePlotItem(pos = pos_array[i] ,color = pg.intColor(pos_array[i][0][2],300,alpha=80),width=0.8, antialias = True)
                widget.addItem(plt)