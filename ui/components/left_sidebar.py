from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_path = os.path.join(base_dir, "assets")
icons_path = os.path.join(assets_path, "icons")

class LeftSideBar(QScrollArea):
    artist_selected = Signal(str)
    playlist_selected = Signal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setWidgetResizable(True)
        
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setObjectName("leftSideBarContent")
        self.outer_layout = QVBoxLayout(self.sidebar_widget)
        
        self.artist_button = QPushButton("Artists")
        self.artist_button.setObjectName("leftSideBarButton")
        self.artist_button.setIconSize(QSize(14, 14))
        self._set_dropdown_icon(self.artist_button, False)
        self.artist_button.clicked.connect(self.toggle_artists)

        self.artist_content = QWidget()
        self.artist_layout = QVBoxLayout(self.artist_content)

        self.artist_content.setVisible(False)

        self.outer_layout.addWidget(self.artist_button)
        self.outer_layout.addWidget(self.artist_content)

        self.playlist_button = QPushButton("Playlists")
        self.playlist_button.setObjectName("leftSideBarButton")
        self.playlist_button.setIconSize(QSize(14, 14))
        self._set_dropdown_icon(self.playlist_button, False)
        self.playlist_button.clicked.connect(self.toggle_playlists)

        self.playlist_content = QWidget()
        self.playlist_layout = QVBoxLayout(self.playlist_content)

        self.playlist_content.setVisible(False)

        self.outer_layout.addWidget(self.playlist_button)
        self.outer_layout.addWidget(self.playlist_content)     

        self.outer_layout.addStretch()

        self.setWidget(self.sidebar_widget)

    def _set_dropdown_icon(self, button, is_open):
        icon_name = "dropdown_open_icon.svg" if is_open else "dropdown_closed_icon.svg"
        button.setIcon(QIcon(os.path.join(icons_path, icon_name)))

    def toggle_artists(self):
        self.artist_content.setVisible(not self.artist_content.isVisible())
        self._set_dropdown_icon(self.artist_button, self.artist_content.isVisible())

    def toggle_playlists(self):
        self.playlist_content.setVisible(not self.playlist_content.isVisible())
        self._set_dropdown_icon(self.playlist_button, self.playlist_content.isVisible())

    def populate_artists(self, artists):
        for i in reversed(range(self.artist_layout.count())):
            widget = self.artist_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        all_artists_button = QPushButton("All Artists")
        all_artists_button.setObjectName("leftSideBarButton")
        all_artists_button.clicked.connect(lambda checked = False, artist_id = "all": self.artist_selected.emit(artist_id))
        
        self.artist_layout.addWidget(all_artists_button, alignment = Qt.AlignLeft)

        for artist in artists:
            button = QPushButton(artist[1])
            button.setObjectName("leftSideBarButton")
            button.clicked.connect(lambda checked = False, artist_id = artist[0]: self.artist_selected.emit(artist_id))

            self.artist_layout.addWidget(button, alignment = Qt.AlignLeft)

        self.artist_layout.addStretch()

    def populate_playlists(self, playlists):
        for i in reversed(range(self.playlist_layout.count())):
            widget = self.playlist_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        all_playlists_button = QPushButton("All Playlists")
        all_playlists_button.setObjectName("leftSideBarButton")
        all_playlists_button.clicked.connect(lambda checked = False, playlist_id = "all": self.playlist_selected.emit(playlist_id))
        
        self.playlist_layout.addWidget(all_playlists_button, alignment = Qt.AlignLeft)

        for playlist in playlists:
            button = QPushButton(playlist[1])
            button.setObjectName("leftSideBarButton")
            button.clicked.connect(lambda checked = False, playlist_id = playlist[0]: self.playlist_selected.emit(playlist_id))

            self.playlist_layout.addWidget(button, alignment = Qt.AlignLeft)

        self.playlist_layout.addStretch()

