from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal

class LeftSideBar(QScrollArea):
    artist_selected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.artists_label = QLabel("Artists")
        self.artists_label.setObjectName("leftSideBarHeading")

        outer_layout = QVBoxLayout()
        self.artist_layout = QVBoxLayout()

        self.artist_layout.addWidget(self.artists_label, alignment = Qt.AlignCenter)
        self.artist_layout.addStretch()

        outer_layout.addLayout(self.artist_layout)

        self.setLayout(outer_layout)

    def populate_artists(self, artists):
        for artist in artists:
            button = QPushButton(artist[1])
            button.setObjectName("leftSideBarButton")
            button.clicked.connect(lambda checked = False, artist_id = artist[0]: self.artist_selected.emit(artist_id))

            self.artist_layout.addWidget(button, alignment = Qt.AlignLeft)

        self.artist_layout.addStretch(1)
