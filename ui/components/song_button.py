from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal, Qt
from ui.components.song_menu import SongMenu

class SongButton(QPushButton):
    song_play_requested = Signal(str)

    def __init__(self, text = "", song_path = "", parent = None):
        super().__init__(text, parent)
        self.song_path = song_path

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_song_menu)

    def show_song_menu(self, position):
        menu = SongMenu(self.song_path, self)

        menu.play_requested.connect(self.handle_play)

        menu.exec(self.mapToGlobal(position))

    def handle_play(self, song_path):
        self.song_play_requested.emit(self.song_path)

    def mouseDoubleClickEvent(self, event):
        self.song_play_requested.emit(self.song_path)
        super().mouseDoubleClickEvent(event)