import os
import sys
import numpy as np
import math
import default_Gcode
import configparser
import print_settings
from print_settings import *


def Gcode_export(full_object):
    print_setting.update()
    for path in full_object:
        if path.E_multiplier ==1 and np.all(path.E_multiplier_array == 1):
            extrusion_multiplier = np.full_like(path.x, EXRTRUSION_MULTIPLIER_DEFAULT)
        elif path.E_multiplier != 1:
            extrusion_multiplier = np.full_like(path.x, path.E_multiplier)
        elif np.any(path.E_multiplier_array != 1):
            extrusion_multiplier = path.E_multiplier_array
        else:
            extrusion_multiplier = np.full_like(path.x, 1)
        
        travel(path.coords[0])
        for i in range(len(path.coords)-1):
            f.write(f'G1 F{PRINT_SPEED_DEFAULT} X{path.x[i+1]+XC:.5f} Y{path.y[i+1]+YC:.5f} Z{path.z[i+1]:.5f} E{path.Eval[i+1] * extrusion_multiplier[i+1]:.5f}\n')

    print("Gcode exported!!")



def travel(coords):
    X = coords[0]
    Y = coords[1]
    Z = coords[2]
    if RETRACTION == True:
        f.write(f'G1 E{-RETRACTION_DISTANCE}\n')
    if Z_HOP == True:
        f.write(f'G91 \n')
        f.write(f'G0 Z{Z_HOP_DISTANCE}\n')
        f.write(f'G90 \n')
        f.write(f'G0 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z+Z_HOP_DISTANCE:.5f}\n' )
        f.write(f'G91 \n')
        f.write(f'G0 Z{-Z_HOP_DISTANCE}\n')
        f.write(f'G90 \n')
    else:
        f.write(f'G0 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z:.5f}\n' )
    if RETRACTION == True:
        f.write(f'G1 E{UNRETRACTION_DISTANCE}\n')

def file_remove():
    f.truncate(0)
    

def start():
    f.write(default_Gcode.startGcode)

def set_temp():
    f.write(f'''M140 S{BED_TEMPERATURE}
M190 S{BED_TEMPERATURE}
M104 S{PRINT_TEMPERATURE}
M109 S{PRINT_TEMPERATURE}
''')

def set_fan_speed():
    f.write(f'M106 S{FAN_SPEED}\n''')
    
def end():
    f.write(default_Gcode.endGcode)

def file_close():
    f.close()


f = open('G-coordinator.gcode', 'w', encoding="UTF-8")



