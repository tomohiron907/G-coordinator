'''
G-coordinator ver 3.0.0
License: MIT
Author: Tomohiro Taniguchi
Usage: 
- Documentation(Japanese): https://qiita.com/tomohiron907/items/747e74965d18f358d852
- GitHub Repository: https://github.com/tomohiron907/G-coordinator/tree/main
'''


#Required Libraries:
#pip install -r requirements.txt

#To execute the G-coordinator, follow these steps:
#1. Change the current directory to "src" by using the command: `cd src`.
#2. Run the "main.py" file by executing the command: `python3 main.py`.



import sys
from PyQt5.QtGui          import *
from PyQt5.QtWidgets      import *
from PyQt5.QtCore         import *
from PyQt5.QtPrintSupport import *
from window.main_window   import main_window, app

def launch():
    icon_path = '../img/G-coordinator.png'
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon) 
    
    main_window.show() 
    sys.exit(app.exec_())

if __name__ == '__main__':
    launch()