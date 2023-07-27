import os
import sys
import traceback
import platform

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *

from window.main.import_file import import_file
from window.draw_object import draw_full_object, draw_object_slider, grid_draw
from window.main.ui_settings import Ui_MainWindow
from window.gcode_export_window import GcodeExportWindow
from window.machine_settings_window import MachineSettingsDialog
from window.app_settings_window import SettingsWindow
from window.main.file_operations import FileOperation

from gcode.gcode_process import Gcode
import path_generator
from path_generator import Path
import qdarktheme


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.new()
        grid_draw(self.graphicsView)
        self.file_operation = FileOperation()

    #=================================================================
    # event handler 
    def draw_updated_object(self):
        """
        reload and draw update object in pyqtgraph widget
        """
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
        
        self.graphicsView.clear()  # initialize pyqtgraph widget
        grid_draw(self.graphicsView)
        draw_full_object(self.graphicsView,self.full_object)  #redraw updated objects in modeling.py
        self.slider_layer.setRange(0, len(self.full_object)-1)  # set slider range
        self.slider_layer.setValue(len(self.full_object)-1)
        self.slider_segment.setRange(0, len(self.full_object[self.slider_layer.value()].coords))
        self.slider_segment.setValue(len(self.full_object[self.slider_layer.value()].coords))
        self.file_save()

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

    def Gcode_create(self):
        Gcode(self.full_object)
        self.message_console.setTextColor(QColor('#00bfff'))
        self.message_console.setText('Gcode Exported')
        self.gcode_window = GcodeExportWindow()
        self.gcode_window.show()

    def open_machine_settings_window(self):
        self.machine_settings_dialog = MachineSettingsDialog()
        self.machine_settings_dialog.show()

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
    
    def closeEvent(self, event):
        with open('buffer/G-coordinator.gcode', 'w') as file:
            file.write('')
        event.accept()
    




    #=================================================================
    # file operartion
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
        self.setWindowTitle("%s - G-coordinator" %(os.path.basename(self.path)
                                                  if self.path else "Untitled"))





    #=================================================================
    # menu bar
    def documentation(self):
        self.menu_bar.documentation(self)

    def version_info(self):
        self.menu_bar.version_info(self)

    def contact_us(self):
        self.menu_bar.contact_us(self)
    
    def run(self):
        self.save_as_modeling()
        self.draw_updated_object()





    #=================================================================
    # other methods
    def print_console(self, message):
        self.message_console.setTextColor(QColor('#ffffff'))
        self.message_console.append(message)
        self.message_console.moveCursor(QTextCursor.End)

    def new(self):
        self.path = None
        with open('buffer/default_start.py', 'r') as file:
            code_str = file.read()

        self.editor.setPlainText(code_str)
        self.update_title()
        

app = QApplication(sys.argv) 
main_window = MainWindow()
main_window.apply_settings()
