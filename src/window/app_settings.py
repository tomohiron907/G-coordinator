import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QColorDialog, QPushButton, QFontDialog, QDialog
from PyQt5.QtCore import QSettings, Qt


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Basic Settings')

        # Font Setting
        font_label = QLabel('Editor Font:')
        self.font_button = QPushButton('Select')
        self.font_button.clicked.connect(self.selectEditorFont)

        # Font Display Label
        self.font_label = QLabel()

        # Font Size Setting
        font_size_label = QLabel('Font Size:')
        self.font_size_lineedit = QLineEdit()

        # Console Font Size Setting
        console_font_size_label = QLabel('Console Font Size:')
        self.console_font_size_lineedit = QLineEdit()

        # Background Color Setting
        background_color_label = QLabel('Background Color:')
        self.background_color_button = QPushButton('Select')
        self.background_color_button.clicked.connect(self.selectBackgroundColor)

        # Background Color Display Label
        self.background_color_label = QLabel()
        self.background_color_label.setFixedSize(30, 30)
        self.background_color_label.setStyleSheet('QLabel { background-color: white; border: 1px solid black; }')

        # Save Button
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.saveSettings)

        # Layout Setup
        layout = QVBoxLayout()
        layout.addWidget(font_label)
        layout.addWidget(self.font_button)
        layout.addWidget(self.font_label)
        layout.addWidget(font_size_label)
        layout.addWidget(self.font_size_lineedit)
        layout.addWidget(console_font_size_label)
        layout.addWidget(self.console_font_size_lineedit)
        layout.addWidget(background_color_label)
        layout.addWidget(self.background_color_button)
        layout.addWidget(self.background_color_label)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.show()

        # Load saved settings
        self.loadSettings()

    def selectEditorFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font_label.setText(font.family())

    def selectBackgroundColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.background_color_label.setStyleSheet(f'QLabel {{ background-color: {color.name()}; border: 1px solid black; }}')

    def saveSettings(self):
        # Save the input settings
        settings = QSettings('settings/app_settings.ini', QSettings.IniFormat)
        settings.setValue('editor/font', self.font_label.text())
        settings.setValue('editor/font_size', self.font_size_lineedit.text())
        settings.setValue('console/font_size', self.console_font_size_lineedit.text())
        settings.setValue('background_color', self.background_color_label.styleSheet())

    def loadSettings(self):
        # Load saved settings
        settings = QSettings('settings/app_settings.ini', QSettings.IniFormat)
        font = settings.value('editor/font')
        font_size = settings.value('editor/font_size')
        console_font_size = settings.value('console/font_size')
        background_color = settings.value('background_color')

        if font is not None:
            self.font_label.setText(font)
        if font_size is not None:
            self.font_size_lineedit.setText(font_size)
        if console_font_size is not None:
            self.console_font_size_lineedit.setText(console_font_size)
        if background_color is not None:
            self.background_color_label.setStyleSheet(background_color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SettingsWindow()
    sys.exit(app.exec_())
