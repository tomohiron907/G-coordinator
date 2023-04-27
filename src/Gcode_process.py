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

            self.retract_setting(path)
            self.z_hop_setting(path)
            extrusion_multiplier = self.ext_multiplier_calc(path)
            feed_speed = self.feed_calc(path)
            self.before_path(path)
            self.travel(path, prev_path) # travel to the first point fo the path // if zhop is true in the previous path, z_hop_down()

            for i in range(len(path.coords)-1):
                self.f.write(f'G1 F{feed_speed[i+1]} X{path.x[i+1]+print_settings.x_origin:.5f} Y{path.y[i+1]+print_settings.y_origin:.5f} Z{path.z[i+1]:.5f} E{path.Eval[i+1] * extrusion_multiplier[i+1]:.5f}\n')
            if path.retraction:
                self.retract()
            if path.z_hop:
                self.z_hop_up()
            self.after_gcode(path)

            prev_path = path
        


    def ext_multiplier_calc(self, path):
        extrusion_multiplier = np.ones(len(path.x))
        if path.extrusion_multiplier is None and any(x is not None for x in path.extrusion_multiplier_array) is False:
            extrusion_multiplier = np.full_like(path.x, print_settings.extrusion_multiplier)
        elif path.extrusion_multiplier != None:
            extrusion_multiplier = np.full_like(path.x, path.extrusion_multiplier)
        elif any(x is not None for x in path.extrusion_multiplier_array):
            for i in range(len(path.extrusion_multiplier_array)):
                if path.extrusion_multiplier_array[i] is not None:
                    extrusion_multiplier[i] = path.extrusion_multiplier_array[i]
        return extrusion_multiplier
    
    def feed_calc(self, path):
        print_speed_array = np.full_like(path.x, print_settings.print_speed)
        if path.print_speed is None and any(x is not None for x in path.print_speed_array) is False:
            pass
            #feed_array = np.full_like(path.x, print_settings.EXRTRUSION_MULTIPLIER_DEFAULT)
        elif path.print_speed != None:
            print_speed_array = np.full_like(path.x, path.print_speed)
        elif any(x is not None for x in path.print_speed_array):
            for i in range(len(path.print_speed_array)):
                if path.print_speed_array[i] is not None:
                    print_speed_array[i] = path.print_speed_array[i]
        return print_speed_array

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


    def retract_setting(self, path):
        if path.retraction is None:
            path.retraction = print_settings.retraction
            #self.retraction = self.retraction
        else:
            pass
    
    def z_hop_setting(self, path):
        if path.z_hop is None:
            path.z_hop = print_settings.z_hop
        else:
            pass
    def z_hop_up(self):
        self.f.write(f'G91 \n')
        self.f.write(f'G0 Z{print_settings.z_hop_distance}\n')
        self.f.write(f'G90 \n')
    def z_hop_down(self):
        self.f.write(f'G91 \n')
        self.f.write(f'G0 Z{-print_settings.z_hop_distance}\n')
        self.f.write(f'G90 \n')
    def retract(self):
        self.f.write(f'G1 E{-print_settings.retraction_distance}\n')
    def unretract(self):
        self.f.write(f'G1 E{print_settings.unretraction_distance}\n')

    def travel(self, path, prev_path):
        X = path.coords[0][0]
        Y = path.coords[0][1]
        Z = path.coords[0][2]
        if prev_path.z_hop:
            self.f.write(f'G0 F{print_settings.travel_speed} X{X+print_settings.x_origin:.5f} Y{Y+print_settings.y_origin:.5f} Z{Z+print_settings.z_hop_distance:.5f}\n' )
        else:
            self.f.write(f'G0 F{print_settings.travel_speed} X{X+print_settings.x_origin:.5f} Y{Y+print_settings.y_origin:.5f} Z{Z:.5f}\n' )

        if prev_path.z_hop:
            self.z_hop_down()
        if prev_path.retraction:
            self.unretract()

    def file_remove(self):
        self.f.truncate(0)

    def file_open(self):
        '''with open ('G-coordinator.gcode', 'w', encoding="UTF-8")as f:
            self.f ='''
        self.f = open('G-coordinator.gcode', 'w', encoding="UTF-8")

    def start_gcode(self):
        self.f.write(default_Gcode.startGcode)

    def set_temperature(self):
        self.f.write(f'''M140 S{print_settings.bed_temperature}
M190 S{print_settings.bed_temperature}
M104 S{print_settings.nozzle_temperature}
M109 S{print_settings.nozzle_temperature}
''')

    def set_fan_speed(self):
        self.f.write(f'M106 S{print_settings.fan_speed}\n''')
        
    def end_gcode(self):
        self.f.write(default_Gcode.endGcode)

    def file_close(self):
        self.f.close()





