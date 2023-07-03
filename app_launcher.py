'''
G-coordinator ver 2.3.0
License: MIT
Author: Tomohiro Taniguchi
Usage: 
- Documentation(Japanese): https://qiita.com/tomohiron907/items/747e74965d18f358d852
- GitHub Repository: https://github.com/tomohiron907/G-coordinator/tree/main
'''

#Required Libraries:
#pip install -r requirements.txt

# You can start G-coordinator in two ways: 
# 1: In the G-coordinator directory, run app_launcher.py
# 2: In the src directory, execute main.py

import os
import sys

if __name__ == '__main__':
    os.chdir('src')
    sys.path.insert(0, '')
    import main

    main.launch()
