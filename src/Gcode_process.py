import os
import sys
import numpy as np
import math
import default_Gcode
import configparser

'''print_setting = configparser.ConfigParser()
print_setting.read('print_setting.ini')'''
ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' # 追加
CONFIG_PATH = ROUTE_PATH + '/print_setting.ini' # 編集
print_setting = configparser.ConfigParser()
print_setting.read(CONFIG_PATH)

NOZZLE = float(print_setting['Nozzle']['nozzle_diameter'])
FILAMENT = float(print_setting['Nozzle']['filament_diameter'])
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
KINEMATICS = print_setting['Kinematics']['Kinematics']
TILT_CODE = print_setting['Kinematics']['Tilt_code']
ROT_CODE = print_setting['Kinematics']['Rot_code']
ROT_OFFSET = float(print_setting['Kinematics']['Rot_offset'])



def Gcode_export(full_object):
    for layer in range(len(full_object)):
        travel(full_object[layer][0][0],full_object[layer][0][1],full_object[layer][0][2],full_object[layer][0][3],full_object[layer][0][4])
        for segment in range(len(full_object[layer])-1):
            x=full_object[layer][segment][0]
            y=full_object[layer][segment][1]
            z=full_object[layer][segment][2]
            tilt=full_object[layer][segment][3] / math.pi * 180.0
            rot=full_object[layer][segment][4] / math.pi * 180.0
            next_x=full_object[layer][segment+1][0]
            next_y=full_object[layer][segment+1][1]
            next_z=full_object[layer][segment+1][2]
            next_tilt=full_object[layer][segment+1][3] / math.pi * 180.0
            next_rot=full_object[layer][segment+1][4] / math.pi * 180.0
            Dis=math.sqrt((next_x-x)**2+(next_y-y)**2+(next_z-z)**2)
            AREA=(NOZZLE-LAYER)*(LAYER)+(LAYER/2)**2*np.pi
            if np.isnan(full_object[layer][segment][6]):
                EXRTRUSION_MULTIPLIER = EXRTRUSION_MULTIPLIER_DEFAULT
            else:
                EXRTRUSION_MULTIPLIER = full_object[layer][segment][6]

            if np.isnan(full_object[layer][segment][5]):
                PRINT_SPEED = PRINT_SPEED_DEFAULT
            else:
                PRINT_SPEED = full_object[layer][segment][5]

            Eval=4*AREA*Dis/(np.pi*FILAMENT**2)*EXRTRUSION_MULTIPLIER
            if KINEMATICS == 'NozzleTilt':
                # In NozzleTilt, the discharge volume is the XYZ displacement.
                f.write(f'G1 F{PRINT_SPEED} X{next_x+XC:.5f} Y{next_y+YC:.5f} Z{next_z:.5f} {TILT_CODE}{next_tilt:.5f} {ROT_CODE}{next_rot+ROT_OFFSET:.5f} E{Eval:.5f}\n')
            elif KINEMATICS == 'BedTiltBC':
                # In BedTilt, the XYZ coordinates change according to Tilt and Rotate.
                # The discharge volume is probably the original XYZ distance traveled.
                f.write(f'G1 F{PRINT_SPEED} X{next_x+XC:.5f} Y{next_y+YC:.5f} Z{next_z:.5f} {TILT_CODE}{next_tilt:.5f} {ROT_CODE}{next_rot+ROT_OFFSET:.5f} E{Eval:.5f}\n')
            else:
                # In Cartesian, the discharge volume is the XYZ movement.
                f.write(f'G1 F{PRINT_SPEED} X{next_x+XC:.5f} Y{next_y+YC:.5f} Z{next_z:.5f} E{Eval:.5f}\n')
    print("Gcode exported!!")



def travel(X,Y,Z,TILT,ROT):
    if RETRACTION == True:
        f.write(f'G1 E{-RETRACTION_DISTANCE}\n')
    if Z_HOP == True:
        f.write(f'G91 \n')
        f.write(f'G0 Z{Z_HOP_DISTANCE}\n')
        f.write(f'G90 \n')
        if KINEMATICS == 'NozzleTilt':
            f.write(f'G0 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z+Z_HOP_DISTANCE:.5f} {TILT_CODE}{TILT:.5f} {ROT_CODE}{ROT+ROT_OFFSET:.5f}\n' )
        elif KINEMATICS == 'BedTiltBC':
            f.write(f'G0 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z+Z_HOP_DISTANCE:.5f} {TILT_CODE}{TILT:.5f} {ROT_CODE}{ROT+ROT_OFFSET:.5f}\n' )
        else:
            f.write(f'G0 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z+Z_HOP_DISTANCE:.5f}\n' )
        f.write(f'G91 \n')
        f.write(f'G0 Z{-Z_HOP_DISTANCE}\n')
        f.write(f'G90 \n')
    else:
        if KINEMATICS == 'NozzleTilt':
            f.write(f'G0 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z:.5f} {TILT_CODE}{TILT:.5f} {ROT_CODE}{ROT+ROT_OFFSET:.5f}\n' )
        elif KINEMATICS == 'BedTiltBC':
            f.write(f'G0 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z:.5f} {TILT_CODE}{TILT:.5f} {ROT_CODE}{ROT+ROT_OFFSET:.5f}\n' )
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



