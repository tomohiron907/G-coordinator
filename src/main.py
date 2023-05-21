import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from window.main_window import *




if __name__ == '__main__':
    app = QApplication(sys.argv) 
    main_window = MainWindow() 
    main_window.show() 
    sys.exit(app.exec_())
