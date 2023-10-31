from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class FileOperation:
    def open(self, main_window):
        # getting path and bool value
        path, _ = QFileDialog.getOpenFileName(main_window, "Open file", "",
                             "Text documents (*.txt);All files (*.*)")
        # if path is true
        if path:
            # try opening path
            try:
                with open(path, 'r') as f:
                    # read the file
                    text = f.read()
            # if some error occurred
            except Exception as e:
                # show error using critical method
                self.dialog_critical(str(e))
            # else
            else:
                # update path value
                main_window.path = path
                # update the text
                main_window.editor.setPlainText(text)
                # update the title
                main_window.update_title()

    def save(self, main_window):
        # if there is no save path
        if main_window.path is None:
            # call save as method
            return main_window.file_save_as()
        # else call save to path method
        #main_window._save_to_path(main_window.path)
        self._save_to_path(main_window, main_window.path)
        # action called by save as action

    def save_as(self, main_window):
        # opening path
        path, _ = QFileDialog.getSaveFileName(main_window, "Save file", "",
                                "Text documents (*.txt);All files (*.*)")
        # if dialog is cancelled i.e no path is selected
        if not path:
            # return this method
            # i.e no action performed
            return
 
        # else call save to path method
        #main_window._save_to_path(path)
        self._save_to_path(main_window, path)

    def _save_to_path(self, main_window, path):
        # get the text
        text = main_window.editor.toPlainText()
        # try catch block
        try:
            # opening file to write
            with open(path, 'w') as f:
                # write text in the file
                f.write(text)

        # if error occurs
        except Exception as e:
            # show error using critical
            main_window.dialog_critical(str(e))

        # else do this
        else:
            # change path
            main_window.path = path
            # update the title
            main_window.update_title()