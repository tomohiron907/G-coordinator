import sys
import os
import traceback
import platform
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import pyqtgraph.opengl as gl
from window.import_file import import_file
import window.editor.syntax_pars
from gcode.gcode_process import Gcode
from  window.draw_object import draw_full_object, draw_object_slider, grid_draw
import configparser
import path_generator
from window.ui_settings import Ui_MainWindow
from window.gcode_export_window import *
from window.machine_settings_window import *
from path_generator import Path
from window.app_settings_window import SettingsWindow
from window.file_operations import FileOperation
from window.parameter_tree import ParameterTree
import qdarktheme


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        grid_draw(self.graphicsView)
        self.file_operation = FileOperation()
    
    def initUI(self):
        self.new()

    def settings(self):
        settings_window = SettingsWindow()
        settings_window.exec_()
        self.apply_settings()

    
    def apply_settings(self):
        settings = QSettings('settings/app_settings.ini', QSettings.IniFormat)
        theme = settings.value('theme')
        font_size = settings.value('editor/font_size')
        console_font_size = settings.value('console/font_size')
        qdarktheme.setup_theme(theme)
        # qtextedit font size changes according to a platform (Don't know why)
        # This is a workaround for now.
        if platform.system() == "Darwin":
            font = QFont('Arial', int(font_size))
        else:
            font = QFont('Arial', int(font_size)-2)
        console_font = QFont('Arial', int(console_font_size))
        self.editor.setFont(font)
        self.line_number_widget.setFontSize(int(font_size))
        self.message_console.setFont(console_font)


    def documentation(self):
        self.menu_bar.documentation(self)

    def version_info(self):
        self.menu_bar.version_info(self)

    def contact_us(self):
        self.menu_bar.contact_us(self)
    
    def run(self):
        self.save_as_modeling()
        self.draw_updated_object()


    # reload and draw update object in pyqtgraph widget
    def draw_updated_object(self):
        Path.count = 0
        print('draw_object')
        
        try:
            #importlib.reload(modeling)  #reload updated modeling.py
            modeling = import_file('buffer/modeling.py')
            self.full_object=modeling.object_modeling()  # get the list of coordinate from modeling.py
            self.full_object = path_generator.flatten_path_list(self.full_object)
            self.message_console.setTextColor(QColor('#00bfff'))
            self.message_console.append('object displyed')
            with open("buffer/modeling.py",'w') as f:
                pass
        except:
            print('syntax error!!')
            self.message_console.setTextColor(QColor('#FF6347'))
            print(str(traceback.format_exc()))
            self.message_console.append(traceback.format_exc())
            with open("buffer/modeling.py",'w') as f:
                pass
        
        #draw_object.set_object_array(self.full_object)
        
        self.graphicsView.clear()  # initialize pyqtgraph widget
        grid_draw(self.graphicsView)
        draw_full_object(self.graphicsView,self.full_object)  #redraw updated objects in modeling.py
        self.slider_layer.setRange(0, len(self.full_object)-1)  # set slider range
        self.slider_layer.setValue(len(self.full_object)-1)
        self.slider_segment.setRange(0, len(self.full_object[self.slider_layer.value()].coords))
        self.slider_segment.setValue(len(self.full_object[self.slider_layer.value()].coords))
        self.file_save()

    def print_console(self, message):
        self.message_console.setTextColor(QColor('#ffffff'))
        self.message_console.append(message)
        self.message_console.moveCursor(QTextCursor.End)


    def Gcode_create(self):
        Gcode(self.full_object)
        self.message_console.setTextColor(QColor('#00bfff'))
        self.message_console.setText('Gcode Exported')
        self.gcode_window = GcodeExportWindow()
        self.gcode_window.show()

    def redraw_layer_object(self): 
        self.graphicsView.clear()  # initialize pyqtgraph widget
        grid_draw(self.graphicsView)
        self.slider_segment.setRange(0, len(self.full_object[self.slider_layer.value()].coords))
        self.slider_segment.setValue(len(self.full_object[self.slider_layer.value()].coords))
        draw_object_slider(self.graphicsView,self.full_object, self.slider_layer.value(),self.slider_segment.value())  #redraw updated objects in modeling.py

    def redraw_segment_object(self): 
        self.graphicsView.clear()  # initialize pyqtgraph widget
        grid_draw(self.graphicsView)
        draw_object_slider(self.graphicsView,self.full_object, self.slider_layer.value(),self.slider_segment.value())  #redraw updated objects in modeling.py
    
    def up_button_pressed(self):
        self.slider_layer.setValue(self.slider_layer.value()+1)
    
    def down_button_pressed(self):
        self.slider_layer.setValue(self.slider_layer.value()-1)
    
    def left_button_pressed(self):
        self.slider_segment.setValue(self.slider_segment.value()-1)
    
    def right_button_pressed(self):
        self.slider_segment.setValue(self.slider_segment.value()+1)

    def new(self):
        #self._save_to_path()
        self.path = None
        with open('buffer/default_start.py', 'r') as file:
            code_str = file.read()

        self.editor.setPlainText(code_str)
        self.update_title()
        
    def file_open(self):
        self.file_operation.open(self)


    def save_as_modeling(self):
        self.file_operation.save_as_modeling(self)

    def file_save(self):
        self.file_operation.save(self)

    def file_save_as(self):
        self.file_operation.save_as(self)


    def update_title(self):
        # setting window title with prefix as file name
        # suffix aas PyQt5 Notepad
        self.setWindowTitle("%s - G-coordinator" %(os.path.basename(self.path)
                                                  if self.path else "Untitled"))



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
    
    def open_machine_settings_window(self):
        
        self.machine_settings_dialog = MachineSettingsDialog()
        self.machine_settings_dialog.show()
    
    def closeEvent(self, event):
        with open('buffer/G-coordinator.gcode', 'w') as file:
            file.write('')

        event.accept()

app = QApplication(sys.argv) 
main_window = MainWindow()
main_window.apply_settings()
