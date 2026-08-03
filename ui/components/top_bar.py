from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
import os

base_dir = os.path.dirname(os.path.abspath((os.path.join(__file__, ".."))))
assets_path = os.path.join(base_dir, "assets")
icons_path = os.path.join(assets_path, "icons")

class TopBar(QWidget):
    def __init__(self, songs_count = 0, artists_count = 0, parent = None):
        super().__init__(parent)

        self.songs_count_label = QLabel(f"{songs_count} Songs")
        self.songs_count_label.setObjectName("topBarLabel")
        self.songs_icon = QLabel()
        pixmap = QPixmap(os.path.join(icons_path, "songs_icon.svg"))
        self.songs_icon.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        self.artists_count_label = QLabel(f"{artists_count} Artists")
        self.artists_count_label.setObjectName("topBarLabel")
        self.artists_icon = QLabel()
        pixmap = QPixmap(os.path.join(icons_path, "artists_icon.svg"))
        self.artists_icon.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.name_label = QLabel("SONUS")
        self.name_label.setObjectName("topBarLabel")

        self.scan_status_label = QLabel("Library up to date")
        self.scan_status_label.setObjectName("topBarLabel")
        success_pixmap = QPixmap(os.path.join(icons_path, "scan_success_icon.svg"))
        scanning_pixmap = QPixmap(os.path.join(icons_path, "scanning_icon.svg"))
        self.success_pixmap = success_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.scanning_pixmap = scanning_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)  
        self.scan_status_icon = QLabel()
        self.scan_status_icon.setPixmap(self.success_pixmap)

        outer_layout = QHBoxLayout()
        left_layout = QHBoxLayout()
        right_layout = QHBoxLayout()

        left_layout.addWidget(self.songs_icon)
        left_layout.addWidget(self.songs_count_label)
        left_layout.addWidget(self.artists_icon)
        left_layout.addWidget(self.artists_count_label)

        right_layout.addWidget(self.scan_status_icon)
        right_layout.addWidget(self.scan_status_label)

        outer_layout.addLayout(left_layout)
        outer_layout.addStretch(1)
        outer_layout.addWidget(self.name_label, 0, Qt.AlignCenter)
        outer_layout.addStretch(1)
        outer_layout.addLayout(right_layout)

        self.setLayout(outer_layout)

    def update_counts(self, songs_count, artists_count):
        self.songs_count_label.setText(f"{songs_count} Songs")
        self.artists_count_label.setText(f"{artists_count} Artists")

    def update_status(self, scanning = False):
        if scanning is True:
            self.scan_status_label.setText("Scanning...")
            self.scan_status_icon.setPixmap(self.scanning_pixmap)

        elif scanning is False:
            self.scan_status_label.setText("Library up to date")
            self.scan_status_icon.setPixmap(self.success_pixmap)
