import configparser
import os



print_setting = configparser.ConfigParser()
#path = os.path.join(os.path.dirname(__file__), 'print_setting.ini')
#print_setting.read(path, encoding='utf-8')
print_setting.read('print_setting.ini')

NOZZLE = float(print_setting['Nozzle']['nozzle_diameter'])
LAYER = float(print_setting['Layer']['Layer_height'])
XC = int(print_setting['Origin']['x_origin'])
YC = int(print_setting['Origin']['y_origin'])
PRINT_SPPED = int(print_setting['Speed']['print_speed'])
TRAVEL_SPEED = int(print_setting['Speed']['travel_speed'])
FAN_SPEED =  int(print_setting['Fan_speed']['fan_speed'])
PRINT_TEMPERATURE = int(print_setting['Temperature']['Nozzle_temperature'])
BED_TEMPERATURE = int(print_setting['Temperature']['Bed_temperature'])
EXRTRUSION_MULTIPLIER = float(print_setting['Extrusion_option']['Extrusion_multiplier'])



startGcode=f"""AnyCubicMega

M201 X1250 Y1250 Z400 E5000 ; sets maximum accelerations, mm/sec^2
M203 X180 Y180 Z12 E80 ; sets maximum feedrates, mm/sec
M204 P1250 R1250 T1250 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X8.00 Y8.00 Z2.00 E10.00 ; sets the jerk limits, mm/sec
M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec


G90 ; use absolute coordinates
M83 ; extruder relative mode
M104 S{PRINT_TEMPERATURE} ; set extruder temp for bed leveling
M140 S{BED_TEMPERATURE}
M109 R{PRINT_TEMPERATURE} ; wait for bed leveling temp
M190 S{BED_TEMPERATURE}
G28 ; home all without mesh bed level
G29 ; mesh bed leveling 
M104 S{PRINT_TEMPERATURE}
G92 E0.0
G1 Y-2.0 X179 F2400
G1 Z30 F720
M109 S{PRINT_TEMPERATURE}

; intro line
G1 X170 F1000
G1 Z0.2 F720
G1 X110.0 E8.0 F900
M73 P0 R91
G1 X40.0 E10.0 F700
G92 E0.0

M221 S100 ; set flow
G21 ; set units to millimeters
G90 ; use absolute coordinates
M83 ; use relative distances for extrusion
M900 K0 ; No linear advance


G92 E0.0

G1 Z0.200 F9000.000


G1 E-3.20000 F4200.00000
G1 Z0.400 F9000.000
G1 X20.0 Y10.0
G1 Z0.300
G1 E3.20000 F2400.00000


M106 S{FAN_SPEED} ; set fan speed

;END OF THE START GCODE


"""




endGcode="""

;START OF THE END GCODE

G1 F2400 E-6
M140 S0
M204 S4000
M205 X20 Y20
M107
M104 S0 ; turn off extruder
M140 S0 ; turn off bed
M84 ; disable motors
M107
G91 ;relative positioning
G1 E-1 F300 ;retract the filament a bit before lifting the nozzle, to release some of the pressure
G1 Z+0.5 E-5 ;move Z up a bit and retract filament even more
G28 X0 ;Y0 ;move X/Y to min endstops, so the head is out of the way
G1 Y180 F2000
M84 ;steppers off
G90
M300 P300 S4000
M82 ;absolute extrusion mode
M104 S0
;End of Gcode
;SETTING_3 {"extruder_quality": ["[general]\\nversion = 4\\nname = Normal 1.0 no
;SETTING_3 zzle vase mode\\ndefinition = anycubic_i3_mega\\n\\n[metadata]\\ninte
;SETTING_3 nt_category = default\\nquality_type = normal\\nposition = 0\\nsettin
;SETTING_3 g_version = 14\\ntype = quality_changes\\n\\n[values]\\ninfill_sparse
;SETTING_3 _density = 5\\nline_width = 1.0\\nmaterial_print_temperature = 220\\n
;SETTING_3 skirt_brim_speed = 20\\nspeed_layer_0 = 10\\nspeed_print = 20\\nspeed
;SETTING_3 _topbottom = 60\\nspeed_wall_0 = 30\\nspeed_wall_x = 30\\ntop_bottom_
;SETTING_3 pattern = lines\\ntop_bottom_thickness = 0.8\\nwall_thickness = 0.8\\
;SETTING_3 n\\n"], "global_quality": "[general]\\nversion = 4\\nname = Normal 1.
;SETTING_3 0 nozzle vase mode\\ndefinition = anycubic_i3_mega\\n\\n[metadata]\\n
;SETTING_3 quality_type = normal\\nsetting_version = 14\\ntype = quality_changes
;SETTING_3 \\n\\n[values]\\nmagic_spiralize = True\\nmaterial_bed_temperature = 
;SETTING_3 65\\nsupport_enable = False\\n\\n"}




"""



