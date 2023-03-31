import configparser
import os
import sys



'''print_setting = configparser.ConfigParser()
print_setting.read('print_setting.ini')'''
ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' # 追加
CONFIG_PATH = ROUTE_PATH + '/print_setting.ini' # 編集
print_setting = configparser.ConfigParser()
print_setting.read(CONFIG_PATH)


START_GCODE_PATH = str(print_setting['Default_gcode']['start_gcode'])
END_GCODE_PATH = str(print_setting['Default_gcode']['end_gcode'])

try:
    with open(START_GCODE_PATH, 'r') as f:
        startGcode = f.read()

    with open(END_GCODE_PATH, 'r') as f :
        endGcode = f.read()

except:
    startGcode = ''
    endGcode = ''

