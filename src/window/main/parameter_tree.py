import sys
import json
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from pyqtgraph.parametertree import ParameterTree as pgParameterTree
from pyqtgraph.parametertree import Parameter

class ParameterTree(pgParameterTree):
    def __init__(self):
        super(ParameterTree, self).__init__()

    def read_setting(self):
        ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' 
        CONFIG_PATH = ROUTE_PATH + '/settings/settings.json'
        with open(CONFIG_PATH, 'r') as f:
            self.settings = json.load(f)

    def parameter_tree_setting(self):
        self.params = [
            {'name': 'nozzle', 'type': 'group', 'children': [
                {'name': 'nozzle_diameter', 'type': 'float', 'value': float(self.settings['Print']['nozzle']['nozzle_diameter'])},
                {'name': 'filament_diameter', 'type': 'float', 'value': float(self.settings['Print']['nozzle']['filament_diameter'])},
            ]},
            {'name': 'layer', 'type': 'group', 'children': [
                {'name': 'layer_height', 'type': 'float', 'value': float(self.settings['Print']['layer']['layer_height'])},
            ]},
            
            {'name': 'speed', 'type': 'group', 'children': [
                {'name': 'print_speed', 'type': 'int', 'value': int(self.settings['Print']['speed']['print_speed'])},
                {'name': 'travel_speed', 'type': 'int', 'value': int(self.settings['Print']['speed']['travel_speed'])},
            ]},
            {'name': 'origin', 'type': 'group', 'children': [
                {'name': 'x', 'type': 'int', 'value': int(self.settings['Print']['origin']['x'])},
                {'name': 'y', 'type': 'int', 'value': int(self.settings['Print']['origin']['y'])},
            ]},
            {'name': 'fan_speed', 'type': 'group', 'children': [
                {'name': 'fan_speed', 'type': 'int', 'value': int(self.settings['Print']['fan_speed']['fan_speed'])},
            ]},
            {'name': 'temperature', 'type': 'group', 'children': [
                {'name': 'nozzle_temperature', 'type': 'int', 'value': int(self.settings['Print']['temperature']['nozzle_temperature'])},
                {'name': 'bed_temperature', 'type': 'int', 'value': int(self.settings['Print']['temperature']['bed_temperature'])},
            ]},
            {'name': 'travel_option', 'type': 'group', 'children': [
                {'name': 'retraction', 'type': 'bool', 'value': bool(self.settings['Print']['travel_option']['retraction'])},
                {'name': 'retraction_distance', 'type': 'float', 'value': float(self.settings['Print']['travel_option']['retraction_distance'])},
                {'name': 'unretraction_distance', 'type': 'float', 'value': float(self.settings['Print']['travel_option']['unretraction_distance'])},
                {'name': 'z_hop', 'type': 'bool', 'value': bool(self.settings['Print']['travel_option']['z_hop'])},
                {'name': 'z_hop_distance', 'type': 'float', 'value': float(self.settings['Print']['travel_option']['z_hop_distance'])},
            ]},
            {'name': 'extrusion_option', 'type': 'group', 'children': [
                {'name': 'extrusion_multiplier', 'type': 'float', 'value': float(self.settings['Print']['extrusion_option']['extrusion_multiplier'])},
            ]},
            
        ]

        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.p.sigTreeStateChanged.connect(self.change)

    

    def change(self, param, changes):
            """
            Update the settings and print the changes made to the console.

            Args:
                param: The parameter that was changed.
                changes: A list of tuples containing the parameter, change type, and new data.

            Returns:
                None
            """
            print("tree changes:")
            for param, change, data in changes:
                path = self.p.childPath(param)
                print(path[0], path[1],":",  str(data))
                self.settings['Print'][path[0]][path[1]] = data
                with open('settings/settings.json', 'w') as f:
                    json.dump(self.settings, f, indent=4)
            print('-------------')

