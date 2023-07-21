import sys
import print_settings
import configparser
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
from pyqtgraph.parametertree import ParameterTree as pgParameterTree
from pyqtgraph.parametertree import Parameter

class ParameterTree(pgParameterTree):
    def __init__(self):
        super(ParameterTree, self).__init__()

    def read_setting(self):
        ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.' # 追加
        CONFIG_PATH = ROUTE_PATH + '/settings/print_settings.ini' # 編集
        self.print_setting = configparser.ConfigParser()
        self.print_setting.read(CONFIG_PATH)

    def parameter_tree_setting(self):
        self.params = [
            {'name': 'nozzle', 'type': 'group', 'children': [
                {'name': 'nozzle_diameter', 'type': 'float', 'value': float(self.print_setting['nozzle']['nozzle_diameter'])},
                {'name': 'filament_diameter', 'type': 'float', 'value': float(self.print_setting['nozzle']['filament_diameter'])},
            ]},
            {'name': 'layer', 'type': 'group', 'children': [
                {'name': 'layer_height', 'type': 'float', 'value': float(self.print_setting['layer']['layer_height'])},
            ]},
            
            {'name': 'speed', 'type': 'group', 'children': [
                {'name': 'print_speed', 'type': 'int', 'value': int(self.print_setting['speed']['print_speed'])},
                {'name': 'travel_speed', 'type': 'int', 'value': int(self.print_setting['speed']['travel_speed'])},
            ]},
            {'name': 'fan_speed', 'type': 'group', 'children': [
                {'name': 'fan_speed', 'type': 'int', 'value': int(self.print_setting['fan_speed']['fan_speed'])},
            ]},
            {'name': 'temperature', 'type': 'group', 'children': [
                {'name': 'nozzle_temperature', 'type': 'int', 'value': int(self.print_setting['temperature']['nozzle_temperature'])},
                {'name': 'bed_temperature', 'type': 'int', 'value': int(self.print_setting['temperature']['bed_temperature'])},
            ]},
            {'name': 'travel_option', 'type': 'group', 'children': [
                {'name': 'retraction', 'type': 'bool', 'value': self.print_setting.getboolean('travel_option','retraction')},
                {'name': 'retraction_distance', 'type': 'float', 'value': float(self.print_setting['travel_option']['retraction_distance'])},
                {'name': 'unretraction_distance', 'type': 'float', 'value': float(self.print_setting['travel_option']['unretraction_distance'])},
                {'name': 'z_hop', 'type': 'bool', 'value': self.print_setting.getboolean('travel_option','z_hop')},
                {'name': 'z_hop_distance', 'type': 'float', 'value': float(self.print_setting['travel_option']['z_hop_distance'])},
            ]},
            {'name': 'extrusion_option', 'type': 'group', 'children': [
                {'name': 'extrusion_multiplier', 'type': 'float', 'value': float(self.print_setting['extrusion_option']['extrusion_multiplier'])},
            ]},
            
        ]

        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.p.sigTreeStateChanged.connect(self.change)

    

    def change(self, param, changes):
        print("tree changes:")
        for param, change, data in changes:
            path = self.p.childPath(param)
            childName = '.'.join(path)
            self.print_setting.set(path[0],path[1],str(data))
            with open('settings/print_settings.ini', 'w') as file:
                self.print_setting.write(file)
            print('  parameter: %s'% childName)
            print('  change:    %s'% change)
            print('  data:      %s'% str(data))
            print('  ----------')
            print_settings.reload_print_setting()


class ParameterTreeWindow(QWidget):
    def __init__(self):
        super(ParameterTreeWindow, self).__init__()
        self.parameter_tree = ParameterTree()
        self.parameter_tree.read_setting()
        self.parameter_tree.parameter_tree_setting()
        self.parameter_tree.setParameters(self.parameter_tree.p, showTop=True)
        layout = QVBoxLayout()
        layout.addWidget(self.parameter_tree)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ParameterTreeWindow()
    mainWindow.show()
    sys.exit(app.exec_())