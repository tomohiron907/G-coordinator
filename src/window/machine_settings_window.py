import sys
import json
from PyQt5.QtGui             import *
from PyQt5.QtWidgets         import *
from PyQt5.QtCore            import *
from PyQt5.QtPrintSupport    import *
from pyqtgraph.parametertree import Parameter, ParameterTree
import configparser

class MachineSettingsDialog(QWidget):
    """
    Machine Settings Window
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Machine Settings")
        self.read_setting()

        # Parameters
        self.params = [
            {'name': 'Hardware', 'type': 'group', 'children': [
                {'name'    : 'kinematics', 'type': 'list', 'values': ['Cartesian', 'NozzleTilt', 'BedTilt', 'BedRotate'], 'value':str(self.settings['Hardware']['kinematics'])},
                {'name'    : 'bed_size', 'type': 'group', 'children': [
                    {'name': 'bed_size_x', 'type': 'int',     'value': float(self.settings['Hardware']['bed_size']['bed_size_x'])},
                    {'name': 'bed_size_y', 'type': 'int',     'value': float(self.settings['Hardware']['bed_size']['bed_size_y'])},
                    {'name': 'bed_size_z', 'type': 'int',     'value': float(self.settings['Hardware']['bed_size']['bed_size_z'])}
                ]}
            ]},
            {'name': 'Kinematics', 'type': 'group', 'children': [
                {'name'    : 'NozzleTilt', 'type': 'group', 'children':[
                    {'name': 'tilt_code', 'type': 'str',      'value': str(self.settings  ['Kinematics']['NozzleTilt']['tilt_code'])},
                    {'name': 'rot_code', 'type': 'str',       'value': str(self.settings  ['Kinematics']['NozzleTilt']['rot_code'])},
                    {'name': 'tilt_offset', 'type': 'float',  'value': float(self.settings['Kinematics']['NozzleTilt']['tilt_offset'])},
                    {'name': 'rot_offset', 'type': 'float',   'value': float(self.settings['Kinematics']['NozzleTilt']['rot_offset'])}
                ]},
                {'name'    : 'BedTiltBC', 'type': 'group', 'children':[
                    {'name': 'tilt_code', 'type': 'str',      'value': str(self.settings  ['Kinematics']['BedTiltBC']['tilt_code'])},
                    {'name': 'rot_code', 'type': 'str',       'value': str(self.settings  ['Kinematics']['BedTiltBC']['rot_code'])},
                    {'name': 'tilt_offset', 'type': 'float',  'value': float(self.settings['Kinematics']['BedTiltBC']['tilt_offset'])},
                    {'name': 'rot_offset', 'type': 'float',   'value': float(self.settings['Kinematics']['BedTiltBC']['rot_offset'])},
                    {'name': 'div_distance', 'type': 'float', 'value': float(self.settings['Kinematics']['BedTiltBC']['div_distance'])}
                ]},
                {'name'    : 'BedRotate', 'type': 'group', 'children':[
                    {'name': 'rot_code', 'type': 'str',       'value': str(self.settings  ['Kinematics']['BedRotate']['rot_code'])},
                    {'name': 'rot_offset', 'type': 'float',   'value': float(self.settings['Kinematics']['BedRotate']['rot_offset'])},
                    {'name': 'div_distance', 'type': 'float', 'value': float(self.settings['Kinematics']['BedRotate']['div_distance'])},

                ]},
                
            ], 'expanded': False},
        ]
        

        self.init_ui()
    
    def init_ui(self):
        """ 
        initialize ui
        """
        layout = QVBoxLayout()
        # Parameter tree
        self.parameter_tree = ParameterTree()
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.parameter_tree.setParameters(self.p)
        self.p.sigTreeStateChanged.connect(self.change)
        layout.addWidget(self.parameter_tree)

        # Start Gcode Editor and gcode 
        start_label = QLabel('Start Gcode Editor', self)
        layout.addWidget(start_label)
        self.start_edit = QPlainTextEdit(self)
        layout.addWidget(self.start_edit)

        start_file_path = 'settings/start_gcode.txt'
        with open(start_file_path, 'r') as file:
            content = file.read()
            self.start_edit.setPlainText(content)

        # End Gcode Editor
        end_label = QLabel('End Gcode Editor', self)
        layout.addWidget(end_label)
        self.end_edit = QPlainTextEdit(self)
        layout.addWidget(self.end_edit)

        end_file_path = 'settings/end_gcode.txt'
        with open(end_file_path, 'r') as file:
            content = file.read()
            self.end_edit.setPlainText(content)



        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        self.setLayout(layout)
    
    def read_setting(self):
        ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' 
        CONFIG_PATH = ROUTE_PATH + '/settings/settings.json'
        with open(CONFIG_PATH, 'r') as f:
            self.settings = json.load(f)

    def change(self, param, changes):
        print("machine tree changes:")
        
        for param, change, data in changes:
            path = self.p.childPath(param)
            # Set section and key based on path length
            if len(path) == 3:
                section, subsection, key = path[0], path[1], path[2]
                self.settings[section][subsection][key] = data
                print(section, subsection, key, ":", data)
            elif len(path) == 2:
                section, key = path[0], path[1]
                self.settings[section][key] = data
                print(section, key, ":", data)
            else:
                continue
        print('-------------')
            
        # Write updated settings to json file
        ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' 
        CONFIG_PATH = ROUTE_PATH + '/settings/settings.json'
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.settings, f, indent=4)



    def save_settings(self):

        start_file_path = 'settings/start_gcode.txt'
        content = self.start_edit.toPlainText()
        with open(start_file_path, 'w') as file:
            file.write(content)


        end_file_path = 'settings/end_gcode.txt'
        content = self.end_edit.toPlainText()
        with open(end_file_path, 'w') as file:
            file.write(content)

        self.close()