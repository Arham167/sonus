from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class LibraryView(QScrollArea):
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

    def display_songs(self, artist, songs):
        while self.songs_layout.count():
            item = self.songs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        artist_label = QLabel(artist[0])
        artist_label.setObjectName("libraryViewArtistLabel")
        self.songs_layout.addWidget(artist_label)

        for song in songs:
            btn = QPushButton(song[1])
            btn.setObjectName("libraryViewSongButton")
            self.songs_layout.addWidget(btn)