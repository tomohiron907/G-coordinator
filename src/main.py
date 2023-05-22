'''
License: MIT
Author: Tomohiro Taniguchi
Usage: 
- Documentation(Japanese): https://qiita.com/tomohiron907/items/747e74965d18f358d852
- GitHub Repository: https://github.com/tomohiron907/G-coordinator/tree/main

Required Libraries:
- pyqt5
- pyqtgraph
- numpy
- pyopengl
- matplotlib
'''



import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from window.main_window import *


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    main_window = MainWindow()
    
    icon_path = '../img/G-coordinator.png'
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon) 

    main_window.show() 
    sys.exit(app.exec_())
