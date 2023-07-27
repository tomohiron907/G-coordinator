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


def extract_variable_names(code_str, names):
    
    try: # try/except for when broken grammar code is sent
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                names.add(node.id)
    except:
        pass
    return names


def extract_function_names(code_string, function_names):
    try: # try/except for when broken grammar code is sent
        def visit_FunctionDef(node):
            function_names.add(node.name)
        tree = ast.parse(code_string)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                visit_FunctionDef(node)
    except:
        pass
    function_names.update(['np.'+method for method in dir(np) if not method.startswith('__')])
    return function_names

def extract_class_names(code_str, names):
    
    try: # try/except for when broken grammar code is sent
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                names.add(node.id)
    except:
        pass
    return names

class Completer(QCompleter):
    def __init__(self,  parent=None):
        super().__init__( parent)
        self.word_list = []
        self.variable_set = set([])
        self.function_set = set([])
        self.class_set = set([])
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setModel(QStringListModel(self.word_list))
        self.activated.connect(self.insertCompletion)

    def set_words(self):
        self.completion_model = QStringListModel(self.word_list)
        self.setModel(self.completion_model)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)

    def insertCompletion(self, completion):
        if self.widget() != self.parent():
            return
        tc = self.parent().textCursor()
        extra = len(completion) - len(self.completionPrefix())
        print(f'{extra=}')
        
        if completion in self.function_set:
            tc.movePosition(QTextCursor.Left)
            tc.movePosition(QTextCursor.EndOfWord)
            if extra == 0:
                tc.insertText("()")
            else:
                tc.insertText(completion[-extra:]+"()")
            tc.movePosition(QTextCursor.PreviousCharacter)
            self.parent().setTextCursor(tc)
        elif completion in self.variable_set:
            tc.movePosition(QTextCursor.Left)
            tc.movePosition(QTextCursor.EndOfWord)
            tc.insertText(completion[-extra:])
            self.parent().setTextCursor(tc)
            tc.movePosition(QTextCursor.Right)
        else:
            tc.insertText(completion[-extra:])

    def update_word_list(self):
        # Initialize the list so that unused variable names, etc. 
        # do not remain in word_list
        self.word_list = [] 
        self.word_list_path_generator(path_generator)
        self.word_list_print_setting(print_settings)
        text = self.parent().toPlainText()

        self.variable_set = extract_variable_names(text, self.variable_set)
        self.function_set = extract_function_names(text, self.function_set)

        cursor_position = self.parent().textCursor().position()
        text_before_cursor = self.parent().toPlainText()[:cursor_position]
        words_before_cursor = text_before_cursor.split()
        completionPrefix = words_before_cursor[-1] if words_before_cursor else "" # 途中までに入植した文字列

        try: # Exclude pre-written strings from the set of names
            self.variable_set.remove(completionPrefix)
            self.function_set.remove(completionPrefix)
        except: # Processing when prefix is not in variables
            pass
        self.word_list += self.variable_set
        self.word_list += self.function_set

        self.word_list = sorted(set(self.word_list))
        
        self.set_words()

    def word_list_path_generator(self, module):
        classes = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(name)
        # Create a word list for autocomplete
        
        for class_name in classes:
            # Add class name
            self.word_list.append(class_name)
            # Get and add methods in the class
            for method_name in dir(getattr(module, class_name)):
                if not method_name.startswith('_'):
                    self.word_list.append(f"{class_name}.{method_name}")

    def word_list_print_setting(self, module):
        self.word_list.append('print_settings')
        for name, obj in inspect.getmembers(module):
            if not name.startswith('_') and not inspect.ismodule(obj):
                self.word_list.append(f'print_settings.{name}')


