from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal

class SongButton(QPushButton):
    doubleClicked = Signal(str)

    def __init__(self, text = "", song_path = "", parent = None):
        super().__init__(text, parent)
        self.song_path = song_path

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit(self.song_path)
        super().mouseDoubleClickEvent(event)