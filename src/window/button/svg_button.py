from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSvg import QSvgRenderer
import sys


class SvgButton(QPushButton):
    def __init__(self, svg_path):
        super().__init__()

        # QSvgRendererを使用してSVGファイルをロード
        self.svg_renderer = QSvgRenderer(svg_path)

        # アイコンのサイズを指定
        icon_size = self.svg_renderer.defaultSize() * 0.2  # サイズを2倍にする例

        # QPixmapを作成し、SVGをレンダリング
        self.default_pixmap = self.render_svg(icon_size, 0.5)
        self.hover_pixmap = self.render_svg(icon_size, 1)

        # QIconを作成し、pixmapを設定
        icon = QIcon(self.default_pixmap)

        # ボタンにアイコンを設定
        self.setIcon(icon)
        self.setIconSize(icon_size)  # アイコンのサイズを設定

        # ボタンのスタイルシートを設定して枠をなくす
        self.setStyleSheet("border: none; background-color: transparent;")

        # ボタンがクリックされたときの処理を定義
        self.clicked.connect(self.on_button_clicked)

    def resize(self, s):
        icon_size = self.svg_renderer.defaultSize() * s  # サイズを2倍にする例

        # QPixmapを作成し、SVGをレンダリング
        self.default_pixmap = self.render_svg(icon_size, 0.5)
        self.hover_pixmap = self.render_svg(icon_size, 1)

        # QIconを作成し、pixmapを設定
        icon = QIcon(self.default_pixmap)

        # ボタンにアイコンを設定
        self.setIcon(icon)
        self.setIconSize(icon_size)  # アイコンのサイズを設定

    def render_svg(self, size, opacity):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)  # 背景を透明に設定
        painter = QPainter(pixmap)
        painter.setOpacity(opacity)
        self.svg_renderer.render(painter)
        del painter  # QPainterオブジェクトを明示的に破棄
        return pixmap

    def enterEvent(self, event):
        # マウスがアイコンに入った時の処理
        icon = QIcon(self.hover_pixmap)
        self.setIcon(icon)

    def leaveEvent(self, event):
        # マウスがアイコンから出た時の処理
        icon = QIcon(self.default_pixmap)
        self.setIcon(icon)

    def on_button_clicked(self):
        print("Button Clicked")

if __name__ == '__main__':
    app = QApplication([])
    svg_path = "open_file.svg"

    button = SvgButton(svg_path)
    button.show()

    app.exec()
