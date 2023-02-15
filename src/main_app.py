import sys
import os
import traceback
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from pyqtgraph.parametertree import Parameter
import pyqtgraph.opengl as gl
import modeling
import importlib
import syntax_pars
import Gcode_process    
import draw_object
import configparser
from gcode_modeling_ui import Ui_MainWindow



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.grid_draw()
    
    def initUI(self):
        self.editor.setStyleSheet("""QPlainTextEdit{ 
            color: #ccc; 
            background-color: #2b2b2b;}""")
        #シンタックス表示
        self.highlight=syntax_pars.PythonHighlighter(self.editor.document())
        self.graphicsView.setCameraPosition(distance=120)
        self.message_console.setReadOnly(True)
        self.message_console.setStyleSheet("background-color: rgb(26, 26, 26);")
        self.up_button.setArrowType(Qt.UpArrow)
        self.down_button.setArrowType(Qt.DownArrow)
        self.read_setting()
        self.parameter_tree_setting()
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.p.sigTreeStateChanged.connect(self.change)
        self.parameter_tree.setParameters(self.p, showTop=True)
        self.parameter_tree.resize(250,540)

    # drawing grid in pyqtgraph widget
    def grid_draw(self):
        gz = gl.GLGridItem()
        gz.setSize(200,200)
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
        
    # reload and draw update object in pyqtgraph widget
    def draw_updated_object(self):
        print('draw_object')
        self.graphicsView.clear()  # initialize pyqtgraph widget
        self.grid_draw()
        try:
            importlib.reload(modeling)  #reload updated modeling.py
            self.full_object=modeling.object_modeling()  # get the list of coordinate from modeling.py
            self.message_console.setTextColor(QColor('#00bfff'))
            self.message_console.setText('object displyed')
            with open("modeling.py",'w') as f:
                pass
        except:
            print('syntax error!!')
            self.message_console.setTextColor(QColor('#FF6347'))
            print(str(traceback.format_exc()))
            self.message_console.setText(traceback.format_exc())
            with open("modeling.py",'w') as f:
                pass
        draw_object.draw_object_array(self.full_object,self.graphicsView,len(self.full_object))  #redraw updated full objects in modeling.py
        self.Slider.setRange(0, len(self.full_object))  # set slider range
        self.file_save()

    def Gcode_create(self):
        importlib.reload(Gcode_process)
        Gcode_process.file_remove()
        Gcode_process.start()
        Gcode_process.set_temp()
        Gcode_process.Gcode_export(self.full_object)
        Gcode_process.end()
        Gcode_process.file_close()
        self.message_console.setTextColor(QColor('#00bfff'))
        self.message_console.setText('Gcode Exported')
        self.gcode_window = GcodeExportWindow()
        self.gcode_window.show()

    def redraw_object(self): 
        #print(self.Slider.value())
        self.graphicsView.clear()  # initialize pyqtgraph widget
        self.grid_draw()
        draw_object.draw_object_array(self.full_object,self.graphicsView,self.Slider.value())  #redraw updated objects in modeling.py
        #print(value)
    
    def up_button_pressed(self):
        self.Slider.setValue(self.Slider.value()+1)
        self.redraw_object()
    
    def down_button_pressed(self):
        self.Slider.setValue(self.Slider.value()-1)
        self.redraw_object()
        
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
        with open('modeling.py', 'w') as f:
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
        self.print_setting = configparser.ConfigParser()
        path = os.path.join(os.path.dirname(__file__), 'print_setting.ini')
        self.print_setting.read(path, encoding='utf-8')

    def parameter_tree_setting(self):
        self.params = [
            {'name': 'Nozzle', 'type': 'group', 'children': [
                {'name': 'Nozzle_diameter', 'type': 'float', 'value': float(self.print_setting['Nozzle']['Nozzle_diameter'])},
            ]},
            {'name': 'Layer', 'type': 'group', 'children': [
                {'name': 'Layer_height', 'type': 'float', 'value': float(self.print_setting['Layer']['Layer_height'])},
            ]},
            {'name': 'Origin', 'type': 'group', 'children': [
                {'name': 'X_origin', 'type': 'int', 'value': int(self.print_setting['Origin']['X_origin'])},
                {'name': 'Y_origin', 'type': 'int', 'value': int(self.print_setting['Origin']['Y_origin'])},
            ]},
            {'name': 'Speed', 'type': 'group', 'children': [
                {'name': 'Print_speed', 'type': 'int', 'value': int(self.print_setting['Speed']['Print_speed'])},
                {'name': 'Travel_speed', 'type': 'int', 'value': int(self.print_setting['Speed']['Travel_speed'])},
            ]},
            {'name': 'Temperature', 'type': 'group', 'children': [
                {'name': 'Nozzle_temperature', 'type': 'int', 'value': int(self.print_setting['Temperature']['Nozzle_temperature'])},
                {'name': 'Bed_temperature', 'type': 'int', 'value': int(self.print_setting['Temperature']['Bed_temperature'])},
            ]},
            {'name': 'Travel_option', 'type': 'group', 'children': [
                {'name': 'Retraction', 'type': 'bool', 'value': self.print_setting.getboolean('Travel_option','Retraction')},
                {'name': 'Retraction_distance', 'type': 'float', 'value': float(self.print_setting['Travel_option']['Retraction_distance'])},
                {'name': 'Unretraction_distance', 'type': 'float', 'value': float(self.print_setting['Travel_option']['Unretraction_distance'])},
                {'name': 'Z_hop', 'type': 'bool', 'value': self.print_setting.getboolean('Travel_option','Z_hop')},
                {'name': 'Z_hop_distance', 'type': 'float', 'value': float(self.print_setting['Travel_option']['Z_hop_distance'])},
            ]},
            {'name': 'Extrusion_option', 'type': 'group', 'children': [
                {'name': 'Extrusion_multiplier', 'type': 'float', 'value': float(self.print_setting['Extrusion_option']['Extrusion_multiplier'])},
            ]},
            
        ]
    

    def change(self, param, changes):
        print("tree changes:")
        for param, change, data in changes:
            path = self.p.childPath(param)
            childName = '.'.join(path)

            self.print_setting.set(path[0],path[1],str(data))
            with open('print_setting.ini', 'w') as file:
                self.print_setting.write(file)
            print('  parameter: %s'% childName)
            print('  change:    %s'% change)
            print('  data:      %s'% str(data))
            print('  ----------')



class GcodeExportWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.save_gocde_button = QPushButton(self)
        self.save_gocde_button.setText('save G-code')
        self.save_gocde_button.pressed.connect(self.file_save_as)
        self.gcode_editor = QTextEdit(self)
        with open('G-coordinator.gcode','r') as f:
            gcode = f.read()
        self.gcode_editor.setPlainText(gcode)
        layout.addWidget(self.save_gocde_button)
        layout.addWidget(self.gcode_editor)
        self.setLayout(layout)
        self.resize(700,500)

    def file_save_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                             "Text documents (*.txt);All files (*.*)")
        if not path:
            return
        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.gcode_editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))



if __name__ == '__main__':
    app = QApplication(sys.argv) 
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'layers.png')
    app.setWindowIcon(QIcon(path))
    main_window = MainWindow() 
    main_window.show() #ウィンドウの表示
    sys.exit(app.exec_()) #プログラム終了
