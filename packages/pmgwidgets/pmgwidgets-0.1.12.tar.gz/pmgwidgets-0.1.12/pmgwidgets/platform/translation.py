import os


def add_translation_file(file_path:str):
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QLocale, QTranslator
    app = QApplication.instance()
    if hasattr(app, 'trans'):
        try:
            tr = QTranslator()
            path = file_path
            tr.load(path)
            app.installTranslator(tr)
        except:
            pass
