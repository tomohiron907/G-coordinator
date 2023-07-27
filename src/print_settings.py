import sys
import configparser
import importlib

from kinematics.kin_base import *
from kinematics.kin_cartesian import *
from kinematics.kin_nozzle_tilt import *
from kinematics.kin_bed_tilt_bc import *
from kinematics.kin_bed_rotate import *

ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' 
CONFIG_PATH = ROUTE_PATH + '/settings/print_settings.ini' 
MACHINE_CONFIG_PATH = ROUTE_PATH + '/settings/machine_settings.ini'

print_setting = configparser.ConfigParser()
print_setting.read(CONFIG_PATH)
machine_settings = configparser.ConfigParser()
machine_settings.read(MACHINE_CONFIG_PATH)

def reload_print_setting():
    global nozzle_diameter, filament_diameter, layer_height, \
        x_origin, y_origin, print_speed, travel_speed, fan_speed, \
        nozzle_temperature, bed_temperature, extrusion_multiplier, \
        retraction, retraction_distance, unretraction_distance, z_hop, z_hop_distance, \
        kin_name, kinematics, bed_x, bed_y, origin_x, origin_y
    print_setting.read(CONFIG_PATH)
    machine_settings.read(MACHINE_CONFIG_PATH)
    nozzle_diameter = float(print_setting['nozzle']['nozzle_diameter'])
    filament_diameter = float(print_setting['nozzle']['filament_diameter'])
    layer_height = float(print_setting['layer']['layer_height'])
    print_speed = int(print_setting['speed']['print_speed'])
    travel_speed = int(print_setting['speed']['travel_speed'])
    fan_speed =  int(print_setting['fan_speed']['fan_speed'])
    nozzle_temperature = int(print_setting['temperature']['nozzle_temperature'])
    bed_temperature = int(print_setting['temperature']['bed_temperature'])
    extrusion_multiplier = float(print_setting['extrusion_option']['extrusion_multiplier'])
    retraction = print_setting.getboolean('travel_option','retraction')
    retraction_distance = float(print_setting['travel_option']['retraction_distance'])
    unretraction_distance = float(print_setting['travel_option']['unretraction_distance'])
    z_hop = print_setting.getboolean('travel_option','z_hop')
    z_hop_distance = float(print_setting['travel_option']['z_hop_distance'])


    bed_x = int(machine_settings['Printer']['bed_size.bed_size_x'])
    bed_y = int(machine_settings['Printer']['bed_size.bed_size_y'])
    x_origin = int(machine_settings['Printer']['origin.origin_x'])
    y_origin = int(machine_settings['Printer']['origin.origin_y'])

    kin_name = machine_settings['Printer']['kinematics']
    if kin_name == 'Cartesian':
        kinematics = Cartesian(machine_settings)
    elif kin_name == 'NozzleTilt':
        kinematics = NozzleTilt(machine_settings)
    elif kin_name == 'BedTilt':
        kinematics = BedTiltBC(machine_settings)
    elif kin_name == 'BedRotate':
        kinematics = BedRotate(machine_settings)
    else:
        kinematics = Kinematics(machine_settings)
    return kin_name, kinematics
nozzle_diameter = None
filament_diameter = None
layer_height = None
x_origin = None
y_origin = None
print_speed = None
travel_speed = None
fan_speed =  None
nozzle_temperature = None
bed_temperature = None
extrusion_multiplier = None
retraction = None
retraction_distance = None
unretraction_distance = None
z_hop = None
z_hop_distance = None

bed_x = None
bed_y = None
origin_x = None
origin_y = None
kin_name = None
kinematics = None
importlib.reload(sys.modules[__name__])

reload_print_setting()