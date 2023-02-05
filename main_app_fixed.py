import sys
import os
import traceback
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import pyqtgraph as pg
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.opengl as gl
import numpy as np
import math
import modeling
import importlib
import syntax_pars
import Gcode_process    
import draw_object
import configparser

'''try:
    import modeling
except:
    pass'''


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        #ウィンドウ設定
        self.setGeometry(0, 0, 1400, 800)
        self.setWindowTitle('Gcode Modeling')
        self.setWindowIcon(QIcon('simulog.gif'))




        #editor 表示ウィジェット
        self.editor = PlainTextEdit(self)
        self.editor.setStyleSheet("""QPlainTextEdit{
            font-family:'Consolas'; 
            color: #ccc; 
            background-color: #2b2b2b;}""")
        #シンタックス表示
        self.highlight=syntax_pars.PythonHighlighter(self.editor.document())
        # setting font to the editor
        self.editor.setGeometry(10,50,400,600)
        #self.editor.setLineWrapMode(PlainTextEdit.LineWrapMode.NoWrap)
        self.path=None
        
        #pyqtgraph 3D表示ウィジェット
        self.w = gl.GLViewWidget(self)
        self.w.setGeometry(440,10,600,770)
        self.w.setCameraPosition(distance=120)
        #self.w.setBackgroundColor('gray')
        gz = gl.GLGridItem()
        gz.setSize(200,200)
        gz.setSpacing(10,10)
        self.w.addItem(gz)
        #self.draw_object()


        #file open button widget
        self.button_open_file=QPushButton("open file",self)
        self.button_open_file.setGeometry(10,5,200,40)
        self.button_open_file.clicked.connect(self.file_open)

        #save button widget
        self.button_open_file=QPushButton("save",self)
        self.button_open_file.setGeometry(210,5,100,40)
        self.button_open_file.clicked.connect(self.file_save)

        #open file button widget
        self.button_open_file=QPushButton("save as",self)
        self.button_open_file.setGeometry(310,5,100,40)
        self.button_open_file.clicked.connect(self.file_saveas)

        #reload button widget
        self.button_reload=QPushButton("reload",self)
        self.button_reload.setGeometry(10,650,400,50)
        self.button_reload.clicked.connect(self.save_as_modeling)
        self.button_reload.clicked.connect(self.draw_updated_object)

        self.msg_box=QTextEdit(self)
        self.msg_box.setGeometry(10,700,400,80)
        self.msg_box.setReadOnly(True)
        self.msg_box.setStyleSheet("background-color: rgb(26, 26, 26);")
        #self.msg_box.setStyleSheet(QColor('#4169e1'))

        #slider widget
        self.sld = QSlider(Qt.Orientation.Vertical, self)
        #self.updateLabel(100)
        self.sld.setGeometry(1035,35,50,630)
        self.sld.setValue(100)
        self.sld.setRange(0, 100)
        
        #self.sld.setTickPosition(QSlider.TicksBothSides)
        self.sld.valueChanged.connect(self.redraw_object)


        self.up_button = QToolButton(self)
        self.up_button.setArrowType(Qt.UpArrow)
        self.up_button.setGeometry(1050,690,20,20)
        self.up_button.clicked.connect(self.up_button_pressed)
        self.down_button = QToolButton(self)
        self.down_button.setArrowType(Qt.DownArrow)
        self.down_button.setGeometry(1050,720,20,20)
        self.down_button.clicked.connect(self.down_button_pressed)


        
        #create Gcode butoon widget
        self.button_Gcode_create=QPushButton("Create Gcode",self)
        self.button_Gcode_create.setGeometry(1140,630,200,40)
        self.button_Gcode_create.clicked.connect(self.Gcode_create)

        self.t = ParameterTree(self)
        self.read_setting()
        self.parameter_tree()
        self.p = Parameter.create(name='params', type='group', children=self.params)
        self.p.sigTreeStateChanged.connect(self.change)
        self.t.setParameters(self.p, showTop=True)
        self.t.setGeometry(1085, 10, 300, 600)



        
    # drawing grid in pyqtgraph widget
    def grid_draw(self):
        gz = gl.GLGridItem()
        gz.setSize(200,200)
        gz.setSpacing(10,10)
        self.w.addItem(gz)




    # reload and draw update object in pyqtgraph widget
    def draw_updated_object(self):
        print('draw_object')
        self.w.clear()  # initialize pyqtgraph widget
        self.grid_draw()
        try:
            importlib.reload(modeling)  #reload updated modeling.py
            self.pos_array=modeling.object_modeling()  # get the list of coordinate from modeling.py
            self.msg_box.setTextColor(QColor('#00bfff'))
            self.msg_box.setText('object displyed')
        except:
            print('syntax error!!')
            self.msg_box.setTextColor(QColor('#FF6347'))
            print(str(traceback.format_exc()))
            self.msg_box.setText(traceback.format_exc())
        draw_object.draw_object_array(self.pos_array,self.w,len(self.pos_array))  #redraw updated full objects in modeling.py
        self.sld.setRange(0, len(self.pos_array))  # set slider range 



    



    def Gcode_create(self):
        importlib.reload(Gcode_process)
        Gcode_process.file_remove()
        Gcode_process.start()
        Gcode_process.Gcode_export(self.pos_array)
        Gcode_process.end()
        Gcode_process.file_close()
        self.msg_box.setTextColor(QColor('#00bfff'))
        self.msg_box.setText('Gcode Exported')


    def redraw_object(self): 
        #print(self.sld.value())
        self.w.clear()  # initialize pyqtgraph widget
        self.grid_draw()
        draw_object.draw_object_array(self.pos_array,self.w,self.sld.value())  #redraw updated objects in modeling.py
        #print(value)
    

    def up_button_pressed(self):
        self.sld.setValue(self.sld.value()+1)
        self.redraw_object()
    
    def down_button_pressed(self):
        self.sld.setValue(self.sld.value()-1)
        self.redraw_object()
    

        
    def file_open(self):
 
        # getting path and bool value
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                             "Text documents (*.txt);All files (*.*)")
        # if path is true
        if path:
            # try opening path
            try:
                with open(path, 'rU') as f:
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
        self.file_save()
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
            return self.file_saveas()
 
        # else call save to path method
        self._save_to_path(self.path)
        # action called by save as action

    def file_saveas(self):
 
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
        self.setWindowTitle("%s - Gcode Modeling" %(os.path.basename(self.path)
                                                  if self.path else "Untitled"))



    def read_setting(self):
        self.print_setting = configparser.ConfigParser()
        self.print_setting.read('print_setting.ini', encoding='utf-8')
        #var = self.print_setting['Nozzle']['Diameter']
        #print(var)

    def parameter_tree(self):
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
                {'name': 'Retraction', 'type': 'bool', 'value': self.print_setting.getboolean('Print_option','Retraction')},
                {'name': 'Retraction_threshold', 'type': 'float', 'value': float(self.print_setting['Print_option']['Retraction_threshold'])},
                {'name': 'Retraction_distance', 'type': 'float', 'value': float(self.print_setting['Print_option']['Retraction_distance'])},
                {'name': 'Unretraction_distance', 'type': 'float', 'value': float(self.print_setting['Print_option']['Unretraction_distance'])},
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








    def keyPressEvent(self, event):
        pass


class PlainTextEdit(QPlainTextEdit):
    def keyPressEvent(self, event):
        #オートインデントの処理
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):

            indent_width = 4
            line_number = self.textCursor().blockNumber()
            #print(line_number)
            line_text = self.document().findBlockByLineNumber(line_number).text()
            indent_level = line_text.count(" " * indent_width)
            if line_text.endswith(":"):
                indent_level += 1
            self.insertPlainText("\n")
            self.insertPlainText( " " * indent_width * indent_level)


            return
        super(PlainTextEdit, self).keyPressEvent(event)



if __name__ == '__main__':
    app = QApplication(sys.argv) #PyQtで必ず呼び出す必要のあるオブジェクト
    main_window = MainWindow() #ウィンドウクラスのオブジェクト生成
    main_window.show() #ウィンドウの表示
    #main_window.draw_object()
    sys.exit(app.exec_()) #プログラム終了
