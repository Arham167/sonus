from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QTimer, QEvent, Qt, Signal
from ui.components.top_bar import TopBar
from ui.components.left_sidebar import LeftSideBar
from ui.components.library_view import LibraryView
from ui.components.right_sidebar import RightSideBar
from ui.components.playback_bar import PlaybackBar

class MainWindow(QMainWindow):
    artist_selected = Signal(str)
    song_selected = Signal(str)
    play_pause = Signal()

    def __init__(self, screen):
        super().__init__()
        self.setWindowTitle("Sonus")

        self.screen_geometry = screen.availableGeometry()
        _, _, width, height = self.screen_geometry.getRect()
        new_w = int(width * 0.9)
        new_h = int(height * 0.9)

        self.setMinimumSize(new_w, new_h)
        
        self.container = QWidget()

        outer_layout = QVBoxLayout(self.container)
        inner_layout = QHBoxLayout()
        inner_left_layout = QVBoxLayout()
        inner_mid_layout = QVBoxLayout()
        inner_right_layout = QVBoxLayout()

        self.top_bar = TopBar()
        outer_layout.addWidget(self.top_bar)

        self.left_sidebar = LeftSideBar()
        inner_left_layout.addWidget(self.left_sidebar)
        self.left_sidebar.artist_selected.connect(self.handle_artist_selection)

        self.library_view = LibraryView()
        inner_mid_layout.addWidget(self.library_view)
        self.library_view.song_selected.connect(self.handle_song_double_click)

        self.right_sidebar = RightSideBar()
        inner_right_layout.addWidget(self.right_sidebar)

        inner_layout.addLayout(inner_left_layout)
        inner_layout.setStretchFactor(inner_left_layout, 1)
        inner_layout.addLayout(inner_mid_layout)
        inner_layout.setStretchFactor(inner_mid_layout, 3)
        inner_layout.addLayout(inner_right_layout)
        inner_layout.setStretchFactor(inner_right_layout, 1)

        outer_layout.addLayout(inner_layout)

        self.playback_bar = PlaybackBar()
        outer_layout.addWidget(self.playback_bar)
        self.playback_bar.play_pause_signal.connect(self.handle_play_pause)

        self.setCentralWidget(self.container)

    def changeEvent(self, event):
        super().changeEvent(event)

        if event.type() != QEvent.WindowStateChange:
            return

        if event.oldState() & Qt.WindowMaximized and not self.isMaximized():
            size = self.size()
            center_x = self.screen_geometry.x() + (self.screen_geometry.width() - size.width()) // 2
            center_y = self.screen_geometry.y() + (self.screen_geometry.height() - size.height()) // 2
            self.move(center_x, center_y)

    def update_topbar(self, songs_count = 0, artists_count = 0, scanning = False):
        self.top_bar.update_counts(songs_count, artists_count)
        self.top_bar.update_status(scanning)

    def update_left_sidebar(self, artists):
        self.left_sidebar.populate_artists(artists)

    def handle_artist_selection(self, artist_id):
        self.artist_selected.emit(artist_id)

    def update_library_view_single(self, artist, songs):
        self.library_view.display_songs_from_artist(artist, songs)

    def update_library_view_all(self, artists, songs):
        self.library_view.display_all_songs(artists, songs)

    def handle_song_double_click(self, path):
        self.song_selected.emit(path)

    def update_playback_state(self, is_playing = False):
        self.playback_bar.update_playback_icon(is_playing)

    def handle_play_pause(self):
        self.play_pause.emit()

    def update_playback_label(self, song, artist, feat_artists):
        self.playback_bar.update_playback_label(song, artist, feat_artists)

    def update_seek_bar_duration(self, duration):
        self.playback_bar.update_duration(duration)

    def update_seek_bar_position(self, position):
        self.playback_bar.update_position(position)