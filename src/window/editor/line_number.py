from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class LineNumberWidget(QTextBrowser):
    def __init__(self, widget: QTextEdit):
        super().__init__()
        self.widget = widget
        self.lineCount = widget.document().blockCount()
        self.fontSize = int(widget.font().pointSizeF())
        self.styleInit()
        self.resize(40, widget.height())
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.verticalScrollBar().setEnabled(False)
        self.verticalScrollBar().setValue(0)

        self.widget.verticalScrollBar().valueChanged.connect(self.__changeLineWidgetScrollAsTargetedWidgetScrollChanged)
        self.initLineCount()

    def __changeLineWidgetScrollAsTargetedWidgetScrollChanged(self, v):
        self.verticalScrollBar().setValue(v)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            self.resize(40, obj.height())
            return True
        return False

    def initLineCount(self):
        for n in range(1, self.lineCount+1):
            self.append(str(n))
    def changeLineCount(self, n):
        max_one = max(self.lineCount, n)
        diff = n - self.lineCount
        if max_one == self.lineCount:
            first_v = self.verticalScrollBar().value()
            for i in range(self.lineCount, self.lineCount + diff, -1):
                self.moveCursor(QTextCursor.End, QTextCursor.MoveAnchor)
                self.moveCursor(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
                self.moveCursor(QTextCursor.End, QTextCursor.KeepAnchor)
                self.textCursor().removeSelectedText()
                self.textCursor().deletePreviousChar()
            last_v = self.verticalScrollBar().value()
            if abs(first_v-last_v) != 2:
                self.verticalScrollBar().setValue(first_v)
        else:
            for i in range(self.lineCount, self.lineCount + diff):
                self.append(str(i + 1))

        self.lineCount = n
        self.styleInit()
        self.verticalScrollBar().setValue(0)


    def setValue(self, v):
        self.verticalScrollBar().setValue(v)

    def setFontSize(self, s: float):
        self.fontSize = int(s)
        self.styleInit()

    def styleInit(self):
        style = '''
            QTextBrowser {
                background: transparent;
                border: none;
                color: #AAA;
                font: ''' + str(self.fontSize) + '''pt;
                text-align: right;
            }
        '''
        self.setStyleSheet(style)
        '''if self.lineCount<99:
            self.setFixedWidth(self.fontSize * 2)
        else:'''
        self.setFixedWidth(self.fontSize * 3)


    def updateLineCount(self):
        new_line_count = self.widget.document().blockCount()
        if new_line_count != self.lineCount:
            self.changeLineCount(new_line_count)