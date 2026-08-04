from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import QTimer, QEvent, Qt, Signal
from ui.components.top_bar import TopBar
from ui.components.left_sidebar import LeftSideBar
from ui.components.library_view import LibraryView
from ui.components.right_sidebar import RightSideBar

class MainWindow(QMainWindow):
    artist_selected = Signal(str)

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

        self.right_sidebar = RightSideBar()
        inner_right_layout.addWidget(self.right_sidebar)

        inner_layout.addLayout(inner_left_layout)
        inner_layout.setStretchFactor(inner_left_layout, 1)
        inner_layout.addLayout(inner_mid_layout)
        inner_layout.setStretchFactor(inner_mid_layout, 3)
        inner_layout.addLayout(inner_right_layout)
        inner_layout.setStretchFactor(inner_right_layout, 1)

        outer_layout.addLayout(inner_layout)

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