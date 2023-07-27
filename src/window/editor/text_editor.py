
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from window.editor.completer import Completer
import path_generator
import print_settings
import numpy as np
import inspect



class TextEditor(QTextEdit):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.completer = Completer(self)
        self.completer.setWidget(self)
        self.trigger = ''
        popup = self.completer.popup()

        popup.setStyleSheet("""
            background-color: rgb(32, 33, 36);
            color: white;
            selection-background-color: rgb(142, 177, 250); /* 選択されているアイテムの背景色 */
            selection-color: black; /* 選択されているアイテムの文字色 */
        """)
        
        self.textChanged.connect(self.completer.update_word_list)


    def print_change(self):
        print('Changed!!')
    def repaint_editor(self):
        print('repaint')
        self.update()
        
    

    def indent(self):
        if not self.textCursor().hasSelection():
            self.insertPlainText(" " * 4)
        #  If there is a selection, insert an indent at the beginning 
        #  of each line within the selection
        else:
            # Get the start and end line numbers of the selected range
            start = self.textCursor().selectionStart()
            end = self.textCursor().selectionEnd()
            start_block = self.document().findBlock(start).blockNumber()
            end_block = self.document().findBlock(end).blockNumber()
            #  Process each row of the selection
            for block_number in range(start_block, end_block + 1):
                block = self.document().findBlockByNumber(block_number)
                cursor = self.textCursor()
                cursor.setPosition(block.position())
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.insertText(" " * 4)

    def unindent(self):
        start = self.textCursor().selectionStart()
        end = self.textCursor().selectionEnd()
        start_block = self.document().findBlock(start).blockNumber()
        end_block = self.document().findBlock(end).blockNumber()

        # Process each row of the selection
        for block_number in range(start_block, end_block + 1):
            block = self.document().findBlockByNumber(block_number)
            cursor = self.textCursor()
            cursor.setPosition(block.position())
            cursor.movePosition(QTextCursor.StartOfLine)

            # Unindent spaces
            line_text = block.text()
            if len(line_text) > 4 and line_text.startswith(" " * 4):
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 4)
                cursor.removeSelectedText()
            elif line_text.startswith(" "):
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
                cursor.removeSelectedText()


    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()
    


    def pastePlainText(self):
        clipboard = QApplication.clipboard()
        plain_text = clipboard.text()
        print(plain_text)
        self.insertPlainText(plain_text)

    def keyPressEvent(self, event):
        # auto_complete
        if self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                self.completer.popup().hide()  # Hide the completion widget when the Enter key is pressed
                event.ignore()
                return
            if event.key() in (Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                self.completer.popup().hide()  
                event.ignore()
                return

        #Auto indentation process
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            indent_width = 4
            line_number = self.textCursor().blockNumber()
            line_text = self.document().findBlockByLineNumber(line_number).text()
            indent_level = line_text.count(" " * indent_width)
            if line_text.endswith(":"):
                indent_level += 1
            self.insertPlainText("\n")
            self.insertPlainText( " " * indent_width * indent_level)
            return
            
        if event.key() == Qt.Key_Tab:
            self.indent()
            return
                
        if event.key() == Qt.Key_Backtab:  
            if event.modifiers() == Qt.ShiftModifier:  # Check if Shift is pressed at the same time
                self.unindent()
                return
            

        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            cursor = self.textCursor()
            position = cursor.position()

            # Get the 4 characters before the cursor
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 4)
            text = cursor.selectedText()

            if text == ' ' * 4:
                # Fix cursor position
                new_position = position - 4
                cursor.setPosition(new_position)

                # Delete 4 spaces at once
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 4)
                cursor.removeSelectedText()

                self.setTextCursor(cursor)
                return
        if event.matches(QKeySequence.Paste):
            print('pasta plain')
            self.pastePlainText()
        else:
            super(TextEditor, self).keyPressEvent(event)


        # auto complete
        cursor_position = self.textCursor().position()
        completionPrefix = self.toPlainText()[:cursor_position].split()[-1]
        if completionPrefix.startswith(self.trigger):
            completionPrefix = completionPrefix[len(self.trigger):]
        else:
            self.completer.popup().hide()
            return
        if len(completionPrefix) < 1:
            self.completer.popup().hide()
            return
        if completionPrefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completionPrefix)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)
