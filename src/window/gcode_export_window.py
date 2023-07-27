
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class GcodeExportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Save G-code file'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        layout = QVBoxLayout()
        self.button = QPushButton('Save G-code file', self)
        self.button.setToolTip('Click to save G-code file')
        self.button.clicked.connect(self.saveFileDialog)
        
        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(QFont("Courier New", 10))
        self.showGCodePreview()
        
        self.label = QLabel(self)
        self.label.setFont(QFont("Arial", 10, QFont.Bold))
        self.label.setText("Showing the first 1000 lines of G-code file.")

        layout.addWidget(self.button)
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
        self.show()

    def showGCodePreview(self):
        with open("buffer/G-coordinator.gcode", 'r') as f:
            content = f.readlines()
            if len(content) > 1000:
                content = content[:1000]
            content = ''.join(content)
            self.textEdit.setPlainText(content)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save G-code file","","G-code Files (*.gcode);;All Files (*)", options=options)
        if fileName:
            with open("buffer/G-coordinator.gcode", 'r') as f:
                content = f.read()
                with open(fileName, 'w') as new_f:
                    new_f.write(content)
            self.showGCodePreview()