import os
import sys
import traceback
import platform
import pickle

from PyQt5.QtCore                   import *
from PyQt5.QtGui                    import *
from PyQt5.QtWidgets                import *
from PyQt5.QtPrintSupport           import *

from window.draw_object             import draw_full_object, draw_object_slider, grid_draw
from window.main.ui_settings        import Ui_MainWindow
from window.gcode_export_window     import GcodeExportWindow
from window.machine_settings_window import MachineSettingsDialog
from window.app_settings_window     import SettingsWindow
from window.main.file_operations    import FileOperation

import gcoordinator as gc
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
        print('draw_object')
        
        try:
            # get code from editor
            with open(main_window.path, 'r') as f:
                self.code = f.read()
            # execute python code. In the code, the full_objects 
            # should be saved in buffer/full_object.pickle
            gc.load_settings('settings/settings.json')
            exec(self.code, globals())
            with open('buffer/full_object.pickle', 'rb') as f:
                self.full_object = pickle.load(f)
            # in full_object list, the elements are Path and Path List
            # make all elements in full_object list to Path
            self.full_object = gc.path_generator.flatten_path_list(self.full_object)
            self.message_console.setTextColor(QColor('#00bfff'))
            self.message_console.append('object displyed')
            
        except:
            # if there is a sytax error in modeling.py, the file is not reloaded
            print('syntax error!!')
            self.message_console.setTextColor(QColor('#FF6347'))
            print(str(traceback.format_exc()))
            self.message_console.append(traceback.format_exc())
            
        # draw updated object in pyqtgraph widget
        self.graphicsView.clear()  
        grid_draw(self.graphicsView)
        draw_full_object(self.graphicsView, self.full_object)  
        self.slider_layer.setRange  (0, len(self.full_object)-1)  
        self.slider_layer.setValue  (   len(self.full_object)-1)
        self.slider_segment.setRange(0, len(self.full_object[self.slider_layer.value()].coords))
        self.slider_segment.setValue(   len(self.full_object[self.slider_layer.value()].coords))
        self.file_save()

    def redraw_layer_object(self): 
        # redraw updated objects according to the layer slider
        self.graphicsView.clear()  
        grid_draw(self.graphicsView)
        self.slider_segment.setRange(0, len(self.full_object[self.slider_layer.value()].coords))
        self.slider_segment.setValue(   len(self.full_object[self.slider_layer.value()].coords))
        draw_object_slider( self.graphicsView,self.full_object, \
                            self.slider_layer.value(),\
                            self.slider_segment.value())  

    def redraw_segment_object(self): 
        # redraw updated objects according to the segment slider
        self.graphicsView.clear()  
        grid_draw(self.graphicsView)
        draw_object_slider( self.graphicsView,self.full_object, \
                            self.slider_layer.value(),\
                            self.slider_segment.value()) 
    
    def up_button_pressed(self):
        self.slider_layer.setValue(self.slider_layer.value()+1)
    
    def down_button_pressed(self):
        self.slider_layer.setValue(self.slider_layer.value()-1)
    
    def left_button_pressed(self):
        self.slider_segment.setValue(self.slider_segment.value()-1)
    
    def right_button_pressed(self):
        self.slider_segment.setValue(self.slider_segment.value()+1)

    def Gcode_create(self):
        self.gcode = gc.GCode(self.full_object)
        self.gcode.start_gcode('settings/start_gcode.txt')
        self.gcode.end_gcode('settings/end_gcode.txt')
        self.gcode.save('buffer/G-coordinator.gcode')
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
        self.file_save()
        self.draw_updated_object()





    #=================================================================
    # other methods
    def print_console(self, message):
        # print message in console
        self.message_console.setTextColor(QColor('#ffffff'))
        self.message_console.append(message)
        self.message_console.moveCursor(QTextCursor.End)

    def new(self):
        # when you open the G-coordinator, this method is called
        # initialize the editor
        self.path = None
        with open('buffer/default_start.py', 'r') as file:
            code_str = file.read()

        self.editor.setPlainText(code_str)
        self.update_title()
        

app = QApplication(sys.argv) 
main_window = MainWindow()
main_window.apply_settings()
