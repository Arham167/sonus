from PySide6.QtWidgets import QApplication
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
style_dir_path = os.path.join(base_dir, "styles")
stylesheet_path = os.path.join(style_dir_path, "stylesheet.qss")

class App(QApplication):
    def __init__(self):
        super().__init__()
        with open(stylesheet_path)  as f:
            self.setStyleSheet(f.read())