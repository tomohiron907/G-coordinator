
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import path_generator
import print_settings
import numpy as np
import inspect



class TextEditor(QTextEdit):
    def __init__(self,  parent=None):
        super().__init__(parent)
        
        self.word_list = ['full_object', 'full_object.append']
        self.class_list = ['full_object']
        self.method_list = ['full_object.append']
        self.variable_list = []
        self.word_list_path_generator(path_generator)
        self.word_list_print_setting(print_settings)
        self.word_list += ["np."+ method  for method in dir(np) if not method.startswith('__')]
        self.method_list += ["np."+ method  for method in dir(np) if not method.startswith('__')]
        completer = QCompleter(self.word_list)
        completer.setModel(QStringListModel(self.word_list))

        self.completer = completer
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)
        self.trigger = ''
        popup = self.completer.popup()

        popup.setStyleSheet("""
            background-color: rgb(32, 33, 36);
            color: white;
            selection-background-color: rgb(142, 177, 250); /* 選択されているアイテムの背景色 */
            selection-color: black; /* 選択されているアイテムの文字色 */
        """)

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







    def insertCompletion(self, completion):
        
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

        
        self.setTextCursor(tc)
    
    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()
    

    def word_list_path_generator(self, module):
        classes = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(name)
                self.class_list.append(name)
        # オートコンプリートに使用するワードリストを作成
        
        for class_name in classes:
            # クラス名を追加
            self.word_list.append(class_name)
            # クラスの中のメソッドを取得して追加
            for method_name in dir(getattr(module, class_name)):
                if not method_name.startswith('_'):
                    self.word_list.append(f"{class_name}.{method_name}")
                    self.method_list.append(f'{class_name}.{method_name}')
        
    def word_list_print_setting(self, module):
        self.word_list.append('print_settings')
        self.class_list.append('print_settings')
        for name, obj in inspect.getmembers(module):
            if not name.startswith('_') and not inspect.ismodule(obj):
                self.word_list.append(f'print_settings.{name}')
                self.variable_list.append(f'print_settings.{name}')


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
        cursor_position = self.textCursor().position()
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
        self.completer.complete(cr)
