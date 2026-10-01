from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal, Qt
from ui.components.song_menu import SongMenu

class SongButton(QPushButton):
    song_play_requested = Signal(str)
    new_playlist_requested = Signal(str)
    add_to_playlist_requested = Signal(str, str)

    def __init__(self, playlists, text = "", song_path = "", parent = None):
        super().__init__(text, parent)
        self.song_path = song_path
        self.playlists = playlists

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_song_menu)

    def show_song_menu(self, position):
        menu = SongMenu(self.song_path, self.playlists, self)

        menu.play_requested.connect(self.handle_play)
        menu.new_requested.connect(self.new_playlist)
        menu.add_requested.connect(self.add_to_playlist)

        menu.exec(self.mapToGlobal(position))

    def handle_play(self, song_path):
        self.song_play_requested.emit(song_path)

    def new_playlist(self, song_path):
        self.new_playlist_requested.emit(song_path)

    def add_to_playlist(self, song_path, playlist_name):
        self.add_to_playlist_requested.emit(song_path, playlist_name)

    def mouseDoubleClickEvent(self, event):
        self.song_play_requested.emit(self.song_path)
        super().mouseDoubleClickEvent(event)