from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os

base_dir = os.path.dirname(os.path.abspath((os.path.join(__file__, ".."))))
assets_path = os.path.join(base_dir, "assets")
icons_path = os.path.join(assets_path, "icons")

class PlaybackBar(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        play_pixmap = QPixmap(os.path.join(icons_path, "play_icon.svg"))
        self.play_pixmap = play_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.play_icon = QLabel()
        self.play_icon.setPixmap(self.play_pixmap)

        outer_layout = QHBoxLayout()
        control_layout = QHBoxLayout()

        control_layout.addWidget(self.play_icon)
        
        outer_layout.addStretch()
        outer_layout.addLayout(control_layout)
        outer_layout.addStretch()

        self.setLayout(outer_layout)