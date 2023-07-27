import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QColorDialog, QPushButton, QFontDialog, QDialog, QRadioButton
from PyQt5.QtCore import QSettings, Qt


class SettingsWindow(QDialog):
    """G-coordinator application settings window

    Args:
        QDialog (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Basic Settings')

        # Theme Selection
        theme_label = QLabel('Theme:')
        self.dark_theme_radio = QRadioButton('Dark')
        self.light_theme_radio = QRadioButton('Light')

        # Font Display Label
        self.font_label = QLabel()

        # Font Size Setting
        font_size_label = QLabel('Font Size:')
        self.font_size_lineedit = QLineEdit()

        # Console Font Size Setting
        console_font_size_label = QLabel('Console Font Size:')
        self.console_font_size_lineedit = QLineEdit()

        # Save Button
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.saveSettings)

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(theme_label)
        layout.addWidget(self.dark_theme_radio)
        layout.addWidget(self.light_theme_radio)
        layout.addWidget(font_size_label)
        layout.addWidget(self.font_size_lineedit)
        layout.addWidget(console_font_size_label)
        layout.addWidget(self.console_font_size_lineedit)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.show()

        # Load saved settings
        self.loadSettings()

    def selectEditorFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_label.setText(font.family())

    

    def saveSettings(self):
        # Save the input settings
        settings = QSettings('settings/app_settings.ini', QSettings.IniFormat)
        settings.setValue('editor/font_size', self.font_size_lineedit.text())
        settings.setValue('console/font_size', self.console_font_size_lineedit.text())
        if self.dark_theme_radio.isChecked():
            settings.setValue('theme', 'dark')
        elif self.light_theme_radio.isChecked():
            settings.setValue('theme', 'light')
        self.close()

    def loadSettings(self):
        # Load saved settings
        settings = QSettings('settings/app_settings.ini', QSettings.IniFormat)
        font_size = settings.value('editor/font_size')
        console_font_size = settings.value('console/font_size')
        theme = settings.value('theme')


        if font_size is not None:
            self.font_size_lineedit.setText(font_size)
        if console_font_size is not None:
            self.console_font_size_lineedit.setText(console_font_size)
        if theme == 'dark':
            self.dark_theme_radio.setChecked(True)
        elif theme == 'light':
            self.light_theme_radio.setChecked(True)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsWindow()
    sys.exit(app.exec_())
