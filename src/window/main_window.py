import sys
import os
import traceback
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.opengl as gl
from import_file import import_file
import syntax_pars
from gcode_process import Gcode
import draw_object
import configparser
import path_generator
from window.ui_settings import Ui_MainWindow
from window.gcode_export_window import *
from window.machine_settings_window import *
from path_generator import Path
from window.app_settings import SettingsWindow
#import markdown2
import qdarktheme

class ReadmeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("README")

        layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

    def set_readme_text(self, readme_text):
        pass
        # Dialog to display readme (not yet completed)
        #html = markdown2.markdown(readme_text)
        #self.text_edit.setHtml(html)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.grid_draw()
    
    def initUI(self):
        #self.setStyleSheet("background-color: rgb(26, 26, 26);")
        menubar = self.menuBar()

        menu_data = {
            'File': {
                'New': {'shortcut': 'Ctrl+N', 'triggered': self.new},
                'Open': {'shortcut': 'Ctrl+O', 'triggered': self.file_open},
                'Save': {'shortcut': 'Ctrl+S', 'triggered': self.file_save},
                'Save As': {'shortcut': 'Ctrl+Shift+S', 'triggered': self.file_save_as}
            },
            'Settings': {
                'Settings': {'shortcut': 'Ctrl+,', 'triggered': self.settings}
            },
            'Edit': {
                'Cut': {'shortcut': 'Ctrl+X'},
                'Copy': {'shortcut': 'Ctrl+C'},
                'Paste': {'shortcut': 'Ctrl+V'},
                'Undo': {'shortcut': 'Ctrl+Z'},
                'Redo': {'shortcut': 'Ctrl+Y'}
            },
            'Run': {
                'Run': {'shortcut': 'Ctrl+R', 'triggered': self.run}
            },
            'Help': {
                #'Documentation': {'triggered': self.documentation},
                'Version Information': {'triggered': self.version_info},
                'Contact Us': {'triggered': self.contact_us}
            }
        }

        for menu_name, actions in menu_data.items():
            menu = menubar.addMenu(menu_name)
            for action_name, action_data in actions.items():
                action = QAction(action_name, self)
                shortcut = action_data.get('shortcut', None)
                triggered = action_data.get('triggered', None)
                if shortcut:
                    action.setShortcut(shortcut)
                if triggered:
                    action.triggered.connect(triggered)
                menu.addAction(action)


        self.editor.setStyleSheet("""QTextEdit{ 
            color: #ccc; 
            background-color: #2b2b2b;}""")
        #シンタックス表示
        self.highlight=syntax_pars.PythonHighlighter(self.editor.document())
        self.graphicsView.setCameraPosition(distance=120)
        self.message_console.setReadOnly(True)
        self.message_console.setStyleSheet("background-color: rgb(26, 26, 26);")
        arrow_style_sheet = """
                            QPushButton {
                                background-color: #3498db;
                                color: #ffffff;
                                border: none;
                                padding: 10px 20px;
                            }
                            QPushButton::up-arrow {
                                image: url("custom_arrow.png");  /* カスタムの矢印画像を指定 */
                                width: 20px;  /* 矢印の幅を指定 */
                                height: 20px;  /* 矢印の高さを指定 */
                            }
                        """
        self.up_button.setArrowType(Qt.UpArrow)
        self.up_button.setStyleSheet(arrow_style_sheet)
        self.down_button.setArrowType(Qt.DownArrow)
        self.left_button.setArrowType(Qt.LeftArrow)
        self.right_button.setArrowType(Qt.RightArrow)
        self.read_setting()
        self.parameter_tree_setting()
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.p.sigTreeStateChanged.connect(self.change)
        self.parameter_tree.setParameters(self.p, showTop=True)
        self.parameter_tree.resize(250,540)
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
        font = QFont('Arial', int(font_size))
        console_font = QFont('Arial', int(console_font_size))
        self.editor.setFont(font)
        self.line_number_widget.setFontSize(int(font_size))
        self.message_console.setFont(console_font)


    def documentation(self):
        # The document menu was once hidden due to problems with the README display,
        #  such as img not being displayed, code highlighting not being done, etc. 
        with open('../README.md', 'r') as file:
            readme_text = file.read()

        dialog = ReadmeDialog(self)
        dialog.set_readme_text(readme_text)
        dialog.exec_()

    def version_info(self):
        version = 'G-coordinator 2.2.0'
        QMessageBox.information(self, 'Version Information', f'Version: {version}')

    def contact_us(self):
        contact = 'tomohiron907@gmail.com'
        QMessageBox.information(self, 'Contact', f'Contact: {contact}\n Twitter: @tamutamu3D')


    # drawing grid in pyqtgraph widget
    def grid_draw(self):
        
        gz = gl.GLGridItem()
        gz.setSize(print_settings.bed_x, print_settings.bed_y)
        gz.setSpacing(10,10)
        axis = gl.GLAxisItem()
        axis.setSize(50,50,50)
        x_text = gl.GLTextItem()
        x_text.setData(pos=(50,0,0),text = 'x')
        y_text = gl.GLTextItem()
        y_text.setData(pos=(0,50,0),text = 'y')
        z_text = gl.GLTextItem()
        z_text.setData(pos=(0,0,50),text = 'z')
        self.graphicsView.addItem(axis)
        self.graphicsView.addItem(x_text)
        self.graphicsView.addItem(y_text)
        self.graphicsView.addItem(z_text)
        self.graphicsView.addItem(gz)
    
    def run(self):
        self.save_as_modeling()
        self.draw_updated_object()


    # reload and draw update object in pyqtgraph widget
    def draw_updated_object(self):
        Path.count = 0
        print('draw_object')
        self.graphicsView.clear()  # initialize pyqtgraph widget
        self.grid_draw()
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
        self.slider_layer.setRange(0, len(self.full_object))  # set slider range
        self.slider_layer.setValue(len(self.full_object))
        self.slider_segment.setRange(0, len(self.full_object[self.slider_layer.value()-1].coords))
        self.slider_segment.setValue(len(self.full_object[self.slider_layer.value()-1].coords))
        draw_object.draw_object_array(self.graphicsView,self.full_object, self.slider_layer.value(),self.slider_segment.value())  #redraw updated objects in modeling.py
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
        self.grid_draw()
        self.slider_segment.setRange(0, len(self.full_object[self.slider_layer.value()-1].coords))
        self.slider_segment.setValue(len(self.full_object[self.slider_layer.value()-1].coords))
        draw_object.draw_object_array(self.graphicsView,self.full_object, self.slider_layer.value(),self.slider_segment.value())  #redraw updated objects in modeling.py

    def redraw_segment_object(self): 
        self.graphicsView.clear()  # initialize pyqtgraph widget
        self.grid_draw()
        draw_object.draw_object_array(self.graphicsView,self.full_object, self.slider_layer.value(),self.slider_segment.value())  #redraw updated objects in modeling.py
    
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
        with open('window/default_start.py', 'r') as file:
            code_str = file.read()

        self.editor.setPlainText(code_str)
        self.update_title()
        
    def file_open(self):
        # getting path and bool value
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                             "Text documents (*.txt);All files (*.*)")
        # if path is true
        if path:
            # try opening path
            try:
                with open(path, 'r') as f:
                    # read the file
                    text = f.read()
            # if some error occurred
            except Exception as e:
                # show error using critical method
                self.dialog_critical(str(e))
            # else
            else:
                # update path value
                self.path = path
                # update the text
                self.editor.setPlainText(text)
                # update the title
                self.update_title()


    def save_as_modeling(self):
        # get the text
        text = self.editor.toPlainText()
        # try catch block
        # opening file to write
        with open('buffer/modeling.py', 'w') as f:
            # write text in the file
            f.write(text)
        #self.draw_object()

    def file_save(self):
        # if there is no save path
        if self.path is None:
            # call save as method
            return self.file_save_as()
        # else call save to path method
        self._save_to_path(self.path)
        # action called by save as action

    def file_save_as(self):
        # opening path
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                             "Text documents (*.txt);All files (*.*)")
        # if dialog is cancelled i.e no path is selected
        if not path:
            # return this method
            # i.e no action performed
            return
 
        # else call save to path method
        self._save_to_path(path)
 
    # save to path method
    def _save_to_path(self, path):
        # get the text
        text = self.editor.toPlainText()
        # try catch block
        try:
            # opening file to write
            with open(path, 'w') as f:
                # write text in the file
                f.write(text)
 
        # if error occurs
        except Exception as e:
            # show error using critical
            self.dialog_critical(str(e))
 
        # else do this
        else:
            # change path
            self.path = path
            # update the title
            self.update_title()

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
