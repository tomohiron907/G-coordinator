import inspect
import re
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import ast

import path_generator
import print_settings
def extract_variable_names(code_str):
    names = set()
    tree = ast.parse(code_str)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)

    print(names)
    return names

class Completer(QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_editor = parent
        
        self.word_list = ['full_object', 'full_object.append']
        self.class_list = ['full_object']
        self.method_list = ['full_object.append']
        self.variable_list = []
        self.word_list_path_generator(path_generator)
        self.word_list_print_setting(print_settings)
        self.word_list += ["np."+ method  for method in dir(np) if not method.startswith('__')]
        self.method_list += ["np."+ method  for method in dir(np) if not method.startswith('__')]
        self.set_words()
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        #self.activated.connect(self.insertCompletion)

    def set_words(self):
        #self.word_list = list(set(self.word_list))
        self.completion_model = QStringListModel(self.word_list)
        #self.setModel(QStringListModel(self.word_list))
        self.setModel(self.completion_model)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)


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

    def update_word_list(self):
        self.word_list = []
        #print(self.text_editor.toPlainText())
        text = self.text_editor.toPlainText()

        # Use regular expression to find variable names followed by '='
        #variable_assignments = re.findall(r'\b([a-zA-Z_]\w*)\s*=', text)

        # Extract the variable names from the matches
        #self.variable_list = [var_name for var_name in variable_assignments]
        self.variable_list = extract_variable_names(text)
        #self.variable_list = list(set(self.va))
        #self.word_list += variable_names
        self.word_list += self.class_list
        self.word_list += self.method_list
        self.word_list += self.variable_list
        self.word_list = list(set(self.word_list))
        self.set_words()

        # Remove duplicates and add new variable names to the words list
        '''unique_variable_names = list(set(variable_names))
        self.completion_model.setStringList(unique_variable_names)'''
    def insertCompletion(self, completion):
        print(f'{completion=}')
        if self.widget() is not None and isinstance(self.widget(), QTextEdit):
            text_edit = self.widget()
            tc = text_edit.textCursor()
            extra = len(completion) - len(self.completionPrefix())
            tc.movePosition(QTextCursor.Left)
            tc.movePosition(QTextCursor.EndOfWord)
            tc.insertText(completion[-extra:])
            text_edit.setTextCursor(tc)
    

    '''def insertCompletion(self, completion):
        
        if self.widget() != self:
            return
        tc = self.textCursor()
        extra = len(completion) - len(self.completionPrefix())
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

