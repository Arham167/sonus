from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal

class SongMenu(QMenu):
    play_requested = Signal(str)
    add_requested = Signal(str)

    def __init__(self, song_path, parent = None):
        super().__init__(parent)
        
        self.song_path = song_path

        play_action = self.addAction("Play")

        play_action.triggered.connect(lambda checked = False: self.play_requested.emit(self.song_path))
