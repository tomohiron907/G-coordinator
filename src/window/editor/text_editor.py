
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

        '''self.completer = Completer(parent=self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)'''
        self.completer = Completer(self)
        self.completer.setWidget(self)
        self.completer.activated.connect(self.completer.insertCompletion)  # CompleterクラスのinsertCompletionを接続

        self.trigger = ''
        popup = self.completer.popup()

        popup.setStyleSheet("""
            background-color: rgb(32, 33, 36);
            color: white;
            selection-background-color: rgb(142, 177, 250); /* 選択されているアイテムの背景色 */
            selection-color: black; /* 選択されているアイテムの文字色 */
        """)
        
        #self.textChanged.connect(lambda: self.completer.update_word_list(text))
        self.textChanged .connect(self.update_text)
        self.update_text()
    
    def update_text(self):
        #self.text = self.toPlainText()
        self.completer.update_word_list()
        #print(self.text)

    def print_change(self):
        print('Changed!!')
    def repaint_editor(self):
        print('repaint')
        self.update()
        
    

    def indent(self):
        if not self.textCursor().hasSelection():
            self.insertPlainText(" " * 4)
        # 選択範囲がある場合は選択範囲内の各行の先頭にインデントを挿入
        else:
            # 選択範囲の開始と終了行番号を取得
            start = self.textCursor().selectionStart()
            end = self.textCursor().selectionEnd()
            start_block = self.document().findBlock(start).blockNumber()
            end_block = self.document().findBlock(end).blockNumber()
            # 選択範囲の各行に対して処理を行う
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

        # 選択範囲の各行に対して処理を行う
        for block_number in range(start_block, end_block + 1):
            block = self.document().findBlockByNumber(block_number)
            cursor = self.textCursor()
            cursor.setPosition(block.position())
            cursor.movePosition(QTextCursor.StartOfLine)

            # スペースをアンインデントする
            line_text = block.text()
            if len(line_text) > 4 and line_text.startswith(" " * 4):
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 4)
                cursor.removeSelectedText()
            elif line_text.startswith(" "):
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 1)
                cursor.removeSelectedText()







    '''def insertCompletion(self, completion):
        
        if self.completer.widget() != self:
            return
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        if extra ==0:
            completion_incert = ''
        else:
            completion_incert = completion[-extra:]
        if not completion in self.method_list:
            tc.insertText(completion_incert)
            if completion == 'Path':
                tc.insertText('()')
                tc.movePosition(QTextCursor.PreviousCharacter)

        else:
            tc.insertText(completion_incert+"()")
            print(completion)
            tc.movePosition(QTextCursor.PreviousCharacter)

        
        self.setTextCursor(tc)'''
    
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
        if self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return
            current_index = self.completer.popup().currentIndex()
            if self.completer.completionModel().data(current_index) == self.textUnderCursor():
                self.completer.popup().hide()
                return

        #オートインデントの処理
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            indent_width = 4
            line_number = self.textCursor().blockNumber()
            #print(line_number)
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
                
        if event.key() == Qt.Key_Backtab:  # Shift + Tabの場合はQt.Key_Backtabを使う
            if event.modifiers() == Qt.ShiftModifier:  # Shiftが同時に押されているかをチェック
                self.unindent()
                return
            

        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            cursor = self.textCursor()
            position = cursor.position()

            # カーソルの前の4文字を取得
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 4)
            text = cursor.selectedText()

            if text == ' ' * 4:
                # カーソル位置を修正
                new_position = position - 4
                cursor.setPosition(new_position)

                # 4つのスペースを一括削除
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 4)
                cursor.removeSelectedText()

                self.setTextCursor(cursor)
                return
        if event.matches(QKeySequence.Paste):
            print('pasta plain')
            self.pastePlainText()
        else:
            super(TextEditor, self).keyPressEvent(event)


        '''cursor_position = self.textCursor().position()
        if cursor_position == 0:
            self.completer.popup().hide()
            return
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
        self.completer.complete(cr)'''
