import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt, QProcess

class TerminalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # テキストエディットウィジェット
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        
        # コマンド入力用のテキストボックス
        self.command_line = QLineEdit()
        self.command_line.returnPressed.connect(self.run_command)
        
        # レイアウト
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.command_line)
        
        # カレントディレクトリの位置を表示
        self.show_current_directory()
        
        # プロセス
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.on_process_output)
        self.process.readyReadStandardError.connect(self.on_process_output)
        
    def show_current_directory(self):
        # カレントディレクトリの位置を取得して表示
        current_directory = os.getcwd()
        self.text_edit.setText(f"Current Directory: {current_directory}")
        
    def run_command(self):
        command = self.command_line.text()
        
        if command:
            # プロセスの開始
            self.text_edit.setText(f"> {command}")
            self.process.start(command)
            self.command_line.clear()
    
    def on_process_output(self):
        # プロセスの出力を取得し、テキストエディットウィジェットに表示
        output = self.process.readAllStandardOutput().data().decode()
        error = self.process.readAllStandardError().data().decode()
        
        if output:
            self.text_edit.setText(output.strip())
        
        if error:
            self.text_edit.setText(f"Error: {error.strip()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main_window = QMainWindow()
    main_window.setWindowTitle("Terminal App")
    main_window.setGeometry(100, 100, 400, 400)
    
    terminal_widget = TerminalWidget()
    main_window.setCentralWidget(terminal_widget)
    
    main_window.show()
    sys.exit(app.exec_())
