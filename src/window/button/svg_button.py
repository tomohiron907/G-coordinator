from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgRenderer
import sys


class SvgButton(QPushButton):
    def __init__(self, svg_path, parent=None):
        super().__init__(parent)

        # Load SVG files using QSvgRenderer
        self.svg_renderer = QSvgRenderer(svg_path)

        # Specify icon size
        icon_size = self.svg_renderer.defaultSize() * 0.2  

        # Create QPixmap and render SVG
        self.default_pixmap = self.render_svg(icon_size, 0.5)
        self.hover_pixmap = self.render_svg(icon_size, 1)

        # Create QIcon and set pixmap
        icon = QIcon(self.default_pixmap)

        # Set an icon on the button
        self.setIcon(icon)
        self.setIconSize(icon_size)  

        # Set up a style sheet for buttons to eliminate borders.
        self.setStyleSheet("border: none; background-color: transparent;")


    def resize(self, s):
        icon_size = self.svg_renderer.defaultSize() * s  

        # Create QPixmap and render SVG
        self.default_pixmap = self.render_svg(icon_size, 0.5)
        self.hover_pixmap = self.render_svg(icon_size, 1)

        # Create QIcon and set pixmap
        icon = QIcon(self.default_pixmap)

        # Set an icon on the button
        self.setIcon(icon)
        self.setIconSize(icon_size)  # Set icon size

    def render_svg(self, size, opacity):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)  # Set background transparent
        painter = QPainter(pixmap)
        painter.setOpacity(opacity)
        self.svg_renderer.render(painter)
        del painter  # Explicitly destroy QPainter objects
        return pixmap

    def enterEvent(self, event):
        # Processing when the mouse enters the icon
        icon = QIcon(self.hover_pixmap)
        self.setIcon(icon)

    def leaveEvent(self, event):
        # Processing when the mouse leaves the icon
        icon = QIcon(self.default_pixmap)
        self.setIcon(icon)


if __name__ == '__main__':
    app = QApplication([])
    svg_path = "window/button/open_file.svg"

    window = QMainWindow()
    window.setGeometry(100, 100, 200, 200) 
    button = SvgButton(svg_path, window)
    button.setGeometry(0, 0, 100, 100)  

    window.show()
    sys.exit(app.exec_())
