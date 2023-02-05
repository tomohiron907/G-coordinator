import numpy as np
import math
import default_Gcode
#import print_setting
import os
import configparser



print_setting = configparser.ConfigParser()
print_setting.read('print_setting.ini', encoding='utf-8')



NOZZLE = float(print_setting['Nozzle']['nozzle_diameter'])
LAYER = float(print_setting['Layer']['Layer_height'])
XC = int(print_setting['Origin']['x_origin'])
YC = int(print_setting['Origin']['y_origin'])
PRINT_SPEED_DEFAULT = int(print_setting['Speed']['print_speed'])
TRAVEL_SPEED = int(print_setting['Speed']['travel_speed'])
PRINT_TEMPERATURE = int(print_setting['Temperature']['Nozzle_temperature'])
BED_TEMPERATURE = int(print_setting['Temperature']['Bed_temperature'])
EXRTRUSION_MULTIPLIER_DEFAULT = float(print_setting['Extrusion_option']['Extrusion_multiplier'])

RETRACTION = print_setting.getboolean('Travel_option','Retraction')
#RETRACTION_THRESHOLD = float(print_setting['Print_option']['Retraction_threshold'])
RETRACTION_DISTANCE = float(print_setting['Travel_option']['Retraction_distance'])
UNRETRACTION_DISTANCE = float(print_setting['Travel_option']['Unretraction_distance'])
Z_HOP = print_setting.getboolean('Travel_option','Z_hop')
Z_HOP_DISTANCE = float(print_setting['Travel_option']['Z_hop_distance'])



def Gcode_export(full_object):
    for layer in range(len(full_object)):
        travel(full_object[layer][0][0],full_object[layer][0][1],full_object[layer][0][2])
        for segment in range(len(full_object[layer])-1):
            x=full_object[layer][segment][0]
            y=full_object[layer][segment][1]
            z=full_object[layer][segment][2]
            next_x=full_object[layer][segment+1][0]
            next_y=full_object[layer][segment+1][1]
            next_z=full_object[layer][segment+1][2]
            Dis=math.sqrt((next_x-x)**2+(next_y-y)**2+(next_z-z)**2)
            AREA=(NOZZLE-LAYER)*(LAYER)+(LAYER/2)**2*np.pi
            if np.isnan(full_object[layer][segment][4]):
                EXRTRUSION_MULTIPLIER = EXRTRUSION_MULTIPLIER_DEFAULT
            else:
                EXRTRUSION_MULTIPLIER = full_object[layer][segment][4]

            if np.isnan(full_object[layer][segment][3]):
                PRINT_SPEED = PRINT_SPEED_DEFAULT
            else:
                PRINT_SPEED = full_object[layer][segment][3]

            Eval=4*AREA*Dis/(np.pi*1.75**2)*EXRTRUSION_MULTIPLIER
            f.write(f'G1 F{PRINT_SPEED} X{next_x+XC:.5f} Y{next_y+YC:.5f} Z{next_z:.5f} E{Eval:.5f}\n')
    print("Gcode exported!!")



def travel(X,Y,Z):
    '''if RETRACTION == False:
        f.write(f'G90 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z:.5f}\n' )
    else:
        f.write(f'G1 E{-RETRACTION_DISTANCE}\n')
        f.write(f'G90 F{TRAVEL_SPEED} X{X+XC:.5f} Y{Y+YC:.5f} Z{Z:.5f}\n' )
        f.write(f'G1 E{UNRETRACTION_DISTANCE}\n')'''

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

    
def end():
    f.write(default_Gcode.endGcode)

def file_close():
    f.close()


f = open('py_modeling.gcode', 'w', encoding="UTF-8")



