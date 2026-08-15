from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
import os

base_dir = os.path.dirname(os.path.abspath((os.path.join(__file__, ".."))))
assets_path = os.path.join(base_dir, "assets")
icons_path = os.path.join(assets_path, "icons")

class PlaybackBar(QWidget):
    play_pause_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon(os.path.join(icons_path, "play_icon.svg")))
        self.play_button.setText("")
        self.play_button.setFlat(True)
        self.play_button.clicked.connect(self.handle_button_click)

        outer_layout = QHBoxLayout()
        control_layout = QHBoxLayout()

        control_layout.addWidget(self.play_button)

        outer_layout.addStretch()
        outer_layout.addLayout(control_layout)
        outer_layout.addStretch()

        self.setLayout(outer_layout)

    def handle_button_click(self):
        self.play_pause_signal.emit()

    def update_playback_icon(self, is_playing):
        if is_playing:
            self.play_button.setIcon(QIcon(os.path.join(icons_path, "pause_icon.svg")))
        else:
            self.play_button.setIcon(QIcon(os.path.join(icons_path, "play_icon.svg")))