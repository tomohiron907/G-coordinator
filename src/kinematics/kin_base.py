import numpy as np
import math

class Kinematics:
    def __init__(self, print_setting):
        self.NOZZLE = float(print_setting['Nozzle']['nozzle_diameter'])
        self.FILAMENT_DIAMETER = float(print_setting['Nozzle']['Filament_diameter'])
        self.LAYER = float(print_setting['Layer']['Layer_height'])
        self.axes_count = 3
        
    def add_parameter_tree(self):
        return None
        
    def e_calc(self, path):
        pass
        
    def draw_object_array(widget,full_object,slider_layer, slider_segment):
        pass