import sys
import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from pyqtgraph import opengl
from window.editor.text_editor import TextEditor
from window.button.svg_button import SvgButton
from window.editor.line_number import LineNumberWidget
from window.editor.syntax_pars import PythonHighlighter
from window.main.parameter_tree import ParameterTree
from window.main.menu_bar import MenuBar

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1400, 800)
        MainWindow.setObjectName("MainWindow")
        self.left_pane_setting(MainWindow)
        self.cetral_pane_setting(MainWindow)
        self.right_pane_setting(MainWindow)

        self.menu_bar = MenuBar()
        self.menu_bar.settings(self)

        self.splitter = QSplitter()
        splitter_style_sheet = """
            QSplitter::handle {
                background: gray;
            }
            QSplitter::handle:horizontal {
                width: 1px;
            }
            QSplitter::handle:vertical {
                height: 1px;
            }
        """
        self.splitter.setStyleSheet(splitter_style_sheet)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.addWidget(QWidget())
        self.splitter.addWidget(QWidget())
        self.splitter.addWidget(QWidget())
        self.splitter.widget(0).setLayout(self.left_pane_layout)
        self.splitter.widget(1).setLayout(self.central_layout)
        self.splitter.widget(2).setLayout(self.right_layout)
        self.splitter.setSizes([300, 600, 220])

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.splitter)
        central_widget = QWidget(MainWindow)
        central_widget.setLayout(self.main_layout)
        MainWindow.setCentralWidget(central_widget)
        MainWindow.setWindowTitle('Splitter with handle')
        
        self.open_button = SvgButton('window/button/open_file.svg', MainWindow)
        self.open_button.resize(0.12)
        self.reload_button = SvgButton('window/button/play.svg', MainWindow)
        self.reload_button.resize(0.3)
        if platform.system() == "Darwin":
            self.open_button.setGeometry(18, 10, 60, 50)
            self.reload_button.setGeometry(78, 10, 60, 50)
        else:
            self.open_button.setGeometry(18, 30, 60, 50)
            self.reload_button.setGeometry(78, 30, 60, 50)


        self.retranslateUi(MainWindow)
        self.signal_connecter(MainWindow)
        
    
    def left_pane_setting(self,MainWindow):
        self.button_style_sheet = """
                                        QPushButton {
                                            background-color: #CCCCCC;
                                            color: #333333;
                                            border: none;
                                            padding: 10px 20px;
                                            border-radius: 10px;
                                        }
                                        QPushButton:hover {
                                            background-color: #AAAAAA;
                                        }
                                    """
        
        
        self.editor =  TextEditor(MainWindow)
        self.editor.setLineWrapMode(TextEditor.LineWrapMode.NoWrap)
        self.editor.textChanged.connect(self.__line_widget_line_count_changed)
        self.editor.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.editor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.editor.setFont(QFont("Arial", 14))
        self.editor.setStyleSheet("""QTextEdit{ 
            color: #ccc; 
            background-color: #2b2b2b;}""")
        self.highlight=PythonHighlighter(self.editor.document())
        self.line_number_widget = LineNumberWidget(self.editor)

        self.line_number_widget.setFontSize(14)
        self.editor_layout = QtWidgets.QHBoxLayout()
        self.editor_layout.addWidget(self.line_number_widget)
        self.editor_layout.addWidget(self.editor)
        self.editor_layout.setSpacing(0)

        self.message_console = QtWidgets.QTextEdit(MainWindow)
        self.message_console.setMinimumHeight(30)
        self.message_console.setReadOnly(True)
        self.message_console.setStyleSheet("background-color: rgb(26, 26, 26);")

        self.left_pane_widget = QWidget(MainWindow)
        self.message_splitter = QSplitter()
        self.message_splitter.setOrientation(Qt.Vertical)
        self.message_splitter.addWidget(QWidget())
        self.message_splitter.widget(0).setLayout(self.editor_layout)
        self.message_splitter.addWidget(self.message_console)
        self.message_splitter.setSizes([10,1])
        
        self.left_pane_layout = QVBoxLayout()
        spacer_widget = QtWidgets.QWidget()
        spacer_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        spacer_widget.setFixedSize(100, 20)
        self.left_pane_layout.addWidget(spacer_widget)
        self.left_pane_layout.addWidget(self.message_splitter)

    def cetral_pane_setting(self, MainWindow):
        self.graphicsView = opengl.GLViewWidget(MainWindow)
        self.graphicsView.setBackgroundColor(QtGui.QColor(30, 30, 30))
        self.graphicsView.setCameraPosition(distance=120)

        self.segment_button_layout = QtWidgets.QHBoxLayout()
        self.slider_segment =  QtWidgets.QSlider(MainWindow)
        self.slider_segment.setOrientation(QtCore.Qt.Horizontal)
        self.left_button = QtWidgets.QToolButton(MainWindow)
        self.right_button = QtWidgets.QToolButton(MainWindow)
        self.segment_button_layout.addWidget(self.slider_segment)
        self.segment_button_layout.addWidget(self.left_button)
        self.segment_button_layout.addWidget(self.right_button)

        self.graphic_seg_layout =  QtWidgets.QVBoxLayout()
        self.graphic_seg_layout.addWidget(self.graphicsView)
        self.graphic_seg_layout.addLayout(self.segment_button_layout)

        self.layer_button_layout = QtWidgets.QVBoxLayout()
        self.slider_layer =  QtWidgets.QSlider(MainWindow)
        self.slider_layer.setOrientation(QtCore.Qt.Vertical)
        self.slider_layout = QtWidgets.QHBoxLayout()
        self.slider_layout.addWidget(self.slider_layer)
        self.slider_layout.setContentsMargins(0, 0, 0, 0)

        self.up_button = QtWidgets.QToolButton(MainWindow)
        self.down_button = QtWidgets.QToolButton(MainWindow)
        self.layer_button_layout.addWidget(self.up_button)
        self.layer_button_layout.addWidget(self.down_button)

        self.layer_layout = QtWidgets.QVBoxLayout()
        self.layer_layout.addLayout(self.slider_layout)
        self.layer_layout.addLayout(self.layer_button_layout)

        self.up_button.setArrowType(Qt.UpArrow)
        self.down_button.setArrowType(Qt.DownArrow)
        self.left_button.setArrowType(Qt.LeftArrow)
        self.right_button.setArrowType(Qt.RightArrow)

        self.central_layout =  QtWidgets.QHBoxLayout()
        self.central_layout.addLayout(self.graphic_seg_layout)
        self.central_layout.addLayout(self.layer_layout)

    def right_pane_setting(self, MainWindow):
        self.machine_settings_button = QtWidgets.QPushButton(MainWindow)
        self.parameter_tree = ParameterTree()
        self.parameter_tree.read_setting()
        self.parameter_tree.parameter_tree_setting()
        self.parameter_tree.setParameters(self.parameter_tree.p, showTop=True)
        self.parameter_tree.resize(250,540)

        self.gcode_export_button = QtWidgets.QPushButton(MainWindow)
        self.gcode_export_button.setStyleSheet(self.button_style_sheet)
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.addWidget(self.machine_settings_button)
        self.right_layout.addWidget(self.parameter_tree)
        self.right_layout.addWidget(self.gcode_export_button)

    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.left_button.setText(_translate("MainWindow", "..."))
        self.right_button.setText(_translate("MainWindow", "..."))
        self.up_button.setText(_translate("MainWindow", "..."))
        self.down_button.setText(_translate("MainWindow", "..."))
        self.gcode_export_button.setText(_translate("MainWindow", "Gcode Export"))
        self.machine_settings_button.setText(_translate("MainWindow", "Machine settings"))
    
    def signal_connecter(self, MainWindow):
        self.open_button.pressed.connect(MainWindow.file_open)
        self.reload_button.pressed.connect(MainWindow.run)
        self.machine_settings_button.pressed.connect(MainWindow.open_machine_settings_window)
        
        self.gcode_export_button.pressed.connect(MainWindow.render_execution_result)
        self.gcode_export_button.pressed.connect(MainWindow.Gcode_create)
        self.slider_layer.valueChanged['int'].connect(MainWindow.redraw_layer_object)
        self.up_button.pressed.connect(MainWindow.up_button_pressed)
        self.down_button.pressed.connect(MainWindow.down_button_pressed)
        self.slider_segment.valueChanged['int'].connect(MainWindow.redraw_segment_object)
        self.left_button.pressed.connect(MainWindow.left_button_pressed)
        self.right_button.pressed.connect(MainWindow.right_button_pressed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def __line_widget_line_count_changed(self):
        if self.line_number_widget:
            n = int(self.editor.document().lineCount())
            self.line_number_widget.changeLineCount(n)
        

