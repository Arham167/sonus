from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from ui.components.song_button import SongButton

class LibraryView(QScrollArea):
    song_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.content = QWidget()
        self.content.setObjectName("libraryContent")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.library_label = QLabel("Library")
        self.library_label.setObjectName("leftSideBarHeading")

        self.songs_layout = QVBoxLayout()

        self.content_layout.addWidget(self.library_label, alignment = Qt.AlignCenter)
        self.content_layout.addLayout(self.songs_layout)
        self.content_layout.addStretch()

        self.setWidget(self.content)

    @staticmethod
    def format_song_display_name(song):
        song_name = song[1].rsplit(".", 1)[0] if "." in song[1] else song[1]
        feat_artist = song[3]

        if feat_artist and feat_artist != "NULL":
            return f"{song_name} ft. {feat_artist}"

        return song_name

    def display_songs_from_artist(self, artist, songs):
        while self.songs_layout.count():
            item = self.songs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        artist_label = QLabel(artist[0])
        artist_label.setObjectName("libraryViewArtistLabel")
        self.songs_layout.addWidget(artist_label)

        for song in songs:
            button = SongButton(self.format_song_display_name(song), song[4])
            button.setObjectName("libraryViewSongButton")
            button.doubleClicked.connect(lambda path: self.song_selected.emit(path))
            self.songs_layout.addWidget(button)

    def display_all_songs(self, artists, songs):
        while self.songs_layout.count():
            item = self.songs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for artist in artists:
            label = QLabel(artist[1])
            label.setObjectName("libraryViewArtistLabel")
            self.songs_layout.addWidget(label)

            for song in songs:
                if song[2] == artist[0]:
                    button = SongButton(self.format_song_display_name(song), song[4])
                    button.setObjectName("libraryViewSongButton")
                    button.doubleClicked.connect(lambda path: self.song_selected.emit(path))
                    self.songs_layout.addWidget(button)
