from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import subprocess


class Terminal(QMainWindow):
    def __init__(self, parent=None):
        super(Terminal, self).__init__(parent)
        self.setupUi()
        self.lineEdit.returnPressed.connect(self.doCMD)
        self.working_dir = "."

    def setupUi(self):
        # self.resize(651, 445)
        self.textBrowser = QTextBrowser(self)
        self.lineEdit = QLineEdit(self)
        self.textBrowser.setStyleSheet(
            "background-color:#2b2b2b; color:white;")

        self.vert_layout = QVBoxLayout()
        self.vert_layout.addWidget(self.textBrowser)
        self.vert_layout.addWidget(self.lineEdit)

        central_widget = QWidget()
        central_widget.setLayout(self.vert_layout)
        self.setCentralWidget(central_widget)

    def doCMD(self):
        cmd = self.lineEdit.text()
        self.lineEdit.setText("")

        if "cd " in cmd:
            vals = cmd.split(" ")
            if vals[1][0] == "/":
                self.working_dir = vals[1]
            else:
                self.working_dir = self.working_dir + "/" + vals[1]

            print(self.working_dir)
            subprocess.call(cmd, shell=True, cwd=self.working_dir)

            self.textBrowser.setText(
                self.textBrowser.toPlainText() + "\n$ " + cmd)

        else:
            self.textBrowser.setTextColor(QColor('#FFFFFF'))
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, shell=True, cwd=self.working_dir, stdin=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                self.textBrowser.setText(
                    self.textBrowser.toPlainText() + "\n$ " + cmd + "\n" + str(e))
            else:
                output, error = process.communicate(
                    input=b"y\n")  # Pass the user input to the subprocess
                if output:
                    self.textBrowser.setText(
                        self.textBrowser.toPlainText() + "\n$ " + cmd + output.decode("utf-8"))
                if error:
                    self.textBrowser.setText(
                        self.textBrowser.toPlainText() + "\n$ " + cmd + error.decode("utf-8"))

        self.textBrowser.verticalScrollBar().setValue(
            self.textBrowser.verticalScrollBar().maximum())

    def get_widget(parent=None):
        return Terminal(parent)
