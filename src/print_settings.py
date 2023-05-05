import sys
import configparser
from kinematics.kin_base import *
from kinematics.kin_cartesian import *

def reload_print_setting():
    global NOZZLE, FILAMENT_DIAMETER, LAYER, XC, YC, \
        PRINT_SPEED_DEFAULT, TRAVEL_SPEED, FAN_SPEED, PRINT_TEMPERATURE, \
        BED_TEMPERATURE, EXRTRUSION_MULTIPLIER_DEFAULT, \
        RETRACTION, RETRACTION_DISTANCE, UNRETRACTION_DISTANCE, Z_HOP, Z_HOP_DISTANCE, \
        KIN_NAME, kinematics
    print_setting.read(CONFIG_PATH)
    NOZZLE = float(print_setting['Nozzle']['nozzle_diameter'])
    FILAMENT_DIAMETER = float(print_setting['Nozzle']['Filament_diameter'])
    LAYER = float(print_setting['Layer']['Layer_height'])
    XC = int(print_setting['Origin']['x_origin'])
    YC = int(print_setting['Origin']['y_origin'])
    PRINT_SPEED_DEFAULT = int(print_setting['Speed']['print_speed'])
    TRAVEL_SPEED = int(print_setting['Speed']['travel_speed'])
    FAN_SPEED =  int(print_setting['Fan_speed']['fan_speed'])
    PRINT_TEMPERATURE = int(print_setting['Temperature']['Nozzle_temperature'])
    BED_TEMPERATURE = int(print_setting['Temperature']['Bed_temperature'])
    EXRTRUSION_MULTIPLIER_DEFAULT = float(print_setting['Extrusion_option']['Extrusion_multiplier'])
    RETRACTION = print_setting.getboolean('Travel_option','Retraction')
    RETRACTION_DISTANCE = float(print_setting['Travel_option']['Retraction_distance'])
    UNRETRACTION_DISTANCE = float(print_setting['Travel_option']['Unretraction_distance'])
    Z_HOP = print_setting.getboolean('Travel_option','Z_hop')
    Z_HOP_DISTANCE = float(print_setting['Travel_option']['Z_hop_distance'])
    KIN_NAME = print_setting['Kinematics']['Kin_name']
    if KIN_NAME == 'Cartesian':
        kinematics = Cartesian(print_setting)

ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' 
CONFIG_PATH = ROUTE_PATH + '/print_setting.ini' 
print_setting = configparser.ConfigParser()

print_setting.read(CONFIG_PATH)

NOZZLE = None
FILAMENT_DIAMETER = None
LAYER = None
XC = None
YC = None
PRINT_SPEED_DEFAULT = None
TRAVEL_SPEED = None
FAN_SPEED =  None
PRINT_TEMPERATURE = None
BED_TEMPERATURE = None
EXRTRUSION_MULTIPLIER_DEFAULT = None
RETRACTION = None
RETRACTION_DISTANCE = None
UNRETRACTION_DISTANCE = None
Z_HOP = None
Z_HOP_DISTANCE = None
KIN_NAME = None
kinematics = None

reload_print_setting()
    

