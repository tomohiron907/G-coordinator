from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
#import markdown2

class MenuBar:
    def settings(self, main_window):
            menubar = main_window.menuBar()

            menu_data = {
                'File': {
                    'New': {'shortcut': 'Ctrl+N', 'triggered': main_window.new},
                    'Open': {'shortcut': 'Ctrl+O', 'triggered': main_window.file_open},
                    'Save': {'shortcut': 'Ctrl+S', 'triggered': main_window.file_save},
                    'Save As': {'shortcut': 'Ctrl+Shift+S', 'triggered': main_window.file_save_as}
                },
                'Settings': {
                    'Settings': {'shortcut': 'Ctrl+,', 'triggered': main_window.settings}
                },
                'Edit': {
                    'Cut': {'shortcut': 'Ctrl+X'},
                    'Copy': {'shortcut': 'Ctrl+C'},
                    'Paste': {'shortcut': 'Ctrl+V'},
                    'Undo': {'shortcut': 'Ctrl+Z'},
                    'Redo': {'shortcut': 'Ctrl+Y'}
                },
                'Run': {
                    'Run': {'shortcut': 'Ctrl+R', 'triggered': main_window.run}
                },
                'Help': {
                    'Documentation': {'triggered': main_window.documentation},
                    'Version Information': {'triggered': main_window.version_info},
                    'Contact Us': {'triggered': main_window.contact_us}
                }
            }

            for menu_name, actions in menu_data.items():
                menu = menubar.addMenu(menu_name)
                for action_name, action_data in actions.items():
                    action = QAction(action_name, main_window)
                    shortcut = action_data.get('shortcut', None)
                    triggered = action_data.get('triggered', None)
                    if shortcut:
                        action.setShortcut(shortcut)
                    if triggered:
                        action.triggered.connect(triggered)
                    menu.addAction(action)
    
    def documentation(self,main_window):
        # The document menu was once hidden due to problems with the README display,
        #  such as img not being displayed, code highlighting not being done, etc. 
        with open('../README.md', 'r') as file:
            readme_text = file.read()

        dialog = ReadmeDialog(main_window)
        dialog.set_readme_text(readme_text)
        dialog.exec_()


    def version_info(self, main_window):
        version = 'G-coordinator 2.2.2'
        QMessageBox.information(main_window, 'Version Information', f'Version: {version}')

    def contact_us(self, main_window):
        contact = 'gcoordinator.3dp@gmail.com'
        QMessageBox.information(main_window, 'Contact', f'Contact: {contact}\n Twitter: @Gcoordinator3DP\n Author: @tamutamu3D')

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