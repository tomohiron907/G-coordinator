import sys
import configparser

ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' 
CONFIG_PATH = ROUTE_PATH + '/print_setting.ini' 
print_setting = configparser.ConfigParser()
print_setting.read(CONFIG_PATH)

nozzle_diameter = float(print_setting['nozzle']['nozzle_diameter'])
filament_diameter = float(print_setting['nozzle']['filament_diameter'])
layer_height = float(print_setting['layer']['layer_height'])
x_origin = int(print_setting['origin']['x_origin'])
y_origin = int(print_setting['origin']['y_origin'])
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

def reload_print_setting():
    global nozzle_diameter, filament_diameter, layer_height, x_origin, y_origin, print_speed, travel_speed, fan_speed, nozzle_temperature, bed_temperature, extrusion_multiplier, retraction, retraction_distance, unretraction_distance, z_hop, z_hop_distance
    print_setting.read(CONFIG_PATH)
    nozzle_diameter = float(print_setting['nozzle']['nozzle_diameter'])
    filament_diameter = float(print_setting['nozzle']['filament_diameter'])
    layer_height = float(print_setting['layer']['layer_height'])
    x_origin = int(print_setting['origin']['x_origin'])
    y_origin = int(print_setting['origin']['y_origin'])
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

