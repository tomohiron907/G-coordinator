import os
import sys
import numpy as np
import math
import default_Gcode
import configparser
import print_settings
from print_settings import *
from path_generator import Path

class Gcode:
    def __init__(self, full_object):
        print_settings.reload_print_setting()
        self.full_object = full_object
        self.file_open()
        self.start_gcode()
        self.set_temperature()
        self.set_fan_speed()
        self.print_full_object()
        self.end_gcode()
        self.file_close()
        print("Gcode exported!!")



    def print_full_object(self):
        print_setting.update()
        prev_path = Path([0,0], [0,0], [0,0])
        for path in self.full_object:


            extrusion_multiplier = self.ext_multiplier_calc(path)
            feed_speed = self.feed_calc(path)
            self.before_path(path)
            self.travel(path) # travel to the first point fo the path
            self.z_hop_down(path, prev_path)
            self.unretract(path, prev_path)
            for i in range(len(path.coords)-1):
                self.f.write(f'G1 F{feed_speed[i+1]} X{path.x[i+1]+XC:.5f} Y{path.y[i+1]+YC:.5f} Z{path.z[i+1]:.5f} E{path.Eval[i+1] * extrusion_multiplier[i+1]:.5f}\n')
            self.after_gcode(path)
            self.retract(path)
            self.z_hop_up(path)
            prev_path = path
        


    def ext_multiplier_calc(self, path):
        extrusion_multiplier = np.ones(len(path.x))
        if path.E_multiplier is None and any(x is not None for x in path.E_multiplier_array) is False:
            extrusion_multiplier = np.full_like(path.x, print_settings.EXRTRUSION_MULTIPLIER_DEFAULT)
        elif path.E_multiplier != None:
            extrusion_multiplier = np.full_like(path.x, path.E_multiplier)
        elif any(x is not None for x in path.E_multiplier_array):
            for i in range(len(path.E_multiplier_array)):
                if path.E_multiplier_array[i] is not None:
                    extrusion_multiplier[i] = path.E_multiplier_array[i]
        return extrusion_multiplier
    
    def feed_calc(self, path):
        feed_array = np.full_like(path.x, print_settings.PRINT_SPEED_DEFAULT)
        if path.feed is None and any(x is not None for x in path.feed_array) is False:
            pass
            #feed_array = np.full_like(path.x, print_settings.EXRTRUSION_MULTIPLIER_DEFAULT)
        elif path.feed != None:
            feed_array = np.full_like(path.x, path.feed)
        elif any(x is not None for x in path.feed_array):
            for i in range(len(path.feed_array)):
                if path.feed_array[i] is not None:
                    feed_array[i] = path.feed_array[i]
        return feed_array

    def before_path(self, path):
        if path.before_gcode is None:
            pass
        else:
            self.f.write(str(path.before_gcode)+'\n')
    
    def after_gcode(self, path):
        if path.after_gcode is None:
            pass
        else:
            self.f.write(str(path.after_gcode)+'\n')

    def z_hop_down(self, path, prev_path):
        if prev_path.z_hop:
            z_hop = prev_path.z_hop
        else:
            z_hop = print_settings.Z_HOP
        if z_hop:
            self.f.write(f'G91 \n')
            self.f.write(f'G0 Z{-Z_HOP_DISTANCE}\n')
            self.f.write(f'G90 \n')
        else:
            pass

    def z_hop_up(self, path):
        if path.z_hop:
            z_hop = path.z_hop
        else:
            z_hop = print_settings.Z_HOP
        if z_hop:
            self.f.write(f'G91 \n')
            self.f.write(f'G0 Z{Z_HOP_DISTANCE}\n')
            self.f.write(f'G90 \n')
        else:
            pass

    
    def retract(self, path):
        if path.retraction:
            retract = path.retraction
        else:
            retract = print_settings.RETRACTION
        if retract:
            self.f.write(f'G1 E{-print_settings.RETRACTION_DISTANCE}\n')
        else:
            pass

    def unretract(self, path, prev_path):
        if prev_path.retraction:
            retract = prev_path.retraction
        else:
            retract = print_settings.RETRACTION
        if retract:
            self.f.write(f'G1 E{print_settings.UNRETRACTION_DISTANCE}\n')
        else:
            pass

    def travel(self, path):
        X = path.coords[0][0]
        Y = path.coords[0][1]
        Z = path.coords[0][2]

        
        self.f.write(f'G0 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z:.5f}\n' )

    def file_remove(self):
        self.f.truncate(0)

    def file_open(self):
        '''with open ('G-coordinator.gcode', 'w', encoding="UTF-8")as f:
            self.f ='''
        self.f = open('G-coordinator.gcode', 'w', encoding="UTF-8")

    def start_gcode(self):
        self.f.write(default_Gcode.startGcode)

    def set_temperature(self):
        self.f.write(f'''M140 S{BED_TEMPERATURE}
M190 S{BED_TEMPERATURE}
M104 S{PRINT_TEMPERATURE}
M109 S{PRINT_TEMPERATURE}
''')

    def set_fan_speed(self):
        self.f.write(f'M106 S{FAN_SPEED}\n''')
        
    def end_gcode(self):
        self.f.write(default_Gcode.endGcode)

    def file_close(self):
        self.f.close()





