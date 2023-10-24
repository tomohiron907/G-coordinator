import sys
from PyQt5.QtGui             import *
from PyQt5.QtWidgets         import *
from PyQt5.QtCore            import *
from PyQt5.QtPrintSupport    import *
from pyqtgraph.parametertree import Parameter, ParameterTree
import configparser
from print_settings          import *

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
            {'name': 'Printer', 'type': 'group', 'children': [
                {'name'    : 'Kinematics', 'type': 'list', 'values': ['Cartesian', 'NozzleTilt', 'BedTilt', 'BedRotate'], 'value':str(self.machine_setting['Printer']['kinematics'])},
                {'name'    : 'bed_size', 'type': 'group', 'children': [
                    {'name': 'bed_size_x', 'type': 'int',     'value': float(self.machine_setting['Printer']['bed_size.bed_size_x'])},
                    {'name': 'bed_size_y', 'type': 'int',     'value': float(self.machine_setting['Printer']['bed_size.bed_size_y'])},
                    {'name': 'bed_size_z', 'type': 'int',     'value': float(self.machine_setting['Printer']['bed_size.bed_size_z'])}
                ]},
                {'name'    : 'origin', 'type': 'group', 'children': [
                    {'name': 'origin_x', 'type': 'int',       'value': float(self.machine_setting['Printer']['origin.origin_x'])},
                    {'name': 'origin_y', 'type': 'int',       'value': float(self.machine_setting['Printer']['origin.origin_y'])}
                ]},
            ]},
            {'name': 'Kinematics', 'type': 'group', 'children': [
                {'name'    : 'NozzleTilt', 'type': 'group', 'children': [
                    {'name': 'tilt_code', 'type': 'str',      'value': str(self.machine_setting['Kinematics']['NozzleTilt.tilt_code'])},
                    {'name': 'rot_code', 'type': 'str',       'value': str(self.machine_setting['Kinematics']['NozzleTilt.rot_code'])},
                    {'name': 'tilt_offset', 'type': 'float',  'value': float(self.machine_setting['Kinematics']['NozzleTilt.tilt_offset'])},
                    {'name': 'rot_offset', 'type': 'float',   'value': float(self.machine_setting['Kinematics']['NozzleTilt.rot_offset'])}
                ]},
                {'name'    : 'BedTilt', 'type': 'group', 'children': [
                    {'name': 'tilt_code', 'type': 'str',      'value': str(self.machine_setting['Kinematics']['BedTilt.tilt_code'])},
                    {'name': 'rot_code', 'type': 'str',       'value': str(self.machine_setting['Kinematics']['BedTilt.rot_code'])},
                    {'name': 'tilt_offset', 'type': 'float',  'value': float(self.machine_setting['Kinematics']['BedTilt.tilt_offset'])},
                    {'name': 'rot_offset', 'type': 'float',   'value': float(self.machine_setting['Kinematics']['BedTilt.rot_offset'])},
                    {'name': 'div_distance', 'type': 'float', 'value': float(self.machine_setting['Kinematics']['BedTilt.div_distance'])}
                ]},
                {'name'    : 'BedRotate', 'type': 'group', 'children': [
                    {'name': 'rot_code', 'type': 'str',       'value': str(self.machine_setting['Kinematics']['BedRotate.rot_code'])},
                    {'name': 'rot_offset', 'type': 'float',   'value': float(self.machine_setting['Kinematics']['BedRotate.rot_offset'])},
                    {'name': 'div_distance', 'type': 'float', 'value': float(self.machine_setting['Kinematics']['BedRotate.div_distance'])},

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
        CONFIG_PATH = ROUTE_PATH + '/settings/machine_settings.ini' 
        self.machine_setting = configparser.ConfigParser()
        self.machine_setting.read(CONFIG_PATH)

    def change(self, param, changes):
        print("machine tree changes:")
        
        for param, change, data in changes:
            path = self.p.childPath(param)
            childName = '.'.join(path)
            # Get the path hierarchy and write the corresponding section and key in the configuration file
            section, key = path[0], '.'.join(path[1:])
            self.machine_setting.set(section, key, str(data))
        
        with open('settings/machine_settings.ini', 'w') as file:
            self.machine_setting.write(file)
        print_settings.reload_print_setting()
        print('  parameter: %s'% childName)
        print('  change:    %s'% change)
        print('  data:      %s'% str(data))
        print('  ----------')


    def save_settings(self):
        print_settings.reload_print_setting()

        start_file_path = 'settings/start_gcode.txt'
        content = self.start_edit.toPlainText()
        with open(start_file_path, 'w') as file:
            file.write(content)


        end_file_path = 'settings/end_gcode.txt'
        content = self.end_edit.toPlainText()
        with open(end_file_path, 'w') as file:
            file.write(content)

        self.close()