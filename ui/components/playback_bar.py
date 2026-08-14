from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import os

base_dir = os.path.dirname(os.path.abspath((os.path.join(__file__, ".."))))
assets_path = os.path.join(base_dir, "assets")
icons_path = os.path.join(assets_path, "icons")

class PlaybackBar(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.is_playing = False

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon(os.path.join(icons_path, "play_icon.svg")))
        self.play_button.setText("")
        self.play_button.setFlat(True)
        self.play_button.clicked.connect(self.toggle_play_pause)

        outer_layout = QHBoxLayout()
        control_layout = QHBoxLayout()

        control_layout.addWidget(self.play_button)
        
        outer_layout.addStretch()
        outer_layout.addLayout(control_layout)
        outer_layout.addStretch()

        self.setLayout(outer_layout)

    def toggle_play_pause(self):
        self.is_playing = not self.is_playing

        if self.is_playing:
            self.play_button.setIcon(QIcon(os.path.join(icons_path, "pause_icon.svg")))
        else:
            self.play_button.setIcon(QIcon(os.path.join(icons_path, "play_icon.svg")))