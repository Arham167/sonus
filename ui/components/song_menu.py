from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal

class SongMenu(QMenu):
    play_requested = Signal(str)
    add_requested = Signal(str, str)
    new_requested = Signal(str)

    def __init__(self, song_path, playlists, parent = None):
        super().__init__(parent)
        
        self.song_path = song_path

        play_action = self.addAction("Play")
        playlist_menu = self.addMenu("Add to Playlist")
        
        for playlist in playlists:
            playlist_button = playlist_menu.addAction(playlist[1])
            playlist_button.triggered.connect(lambda checked = False, name = playlist[1]: self.add_requested.emit(self.song_path, name))

        new_action = playlist_menu.addAction("<New Playlist>")

        play_action.triggered.connect(lambda checked = False: self.play_requested.emit(self.song_path))
        new_action.triggered.connect(lambda checked = False: self.new_requested.emit(self.song_path))