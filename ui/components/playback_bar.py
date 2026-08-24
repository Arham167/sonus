from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSlider
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon
import os

base_dir = os.path.dirname(os.path.abspath((os.path.join(__file__, ".."))))
assets_path = os.path.join(base_dir, "assets")
icons_path = os.path.join(assets_path, "icons")

class PlaybackBar(QWidget):
    play_pause_signal = Signal()

    @staticmethod
    def format_time(milliseconds):
        total_seconds = milliseconds // 1000
        minutes, seconds = divmod(total_seconds, 60)

        return f"{minutes}:{seconds:02}"


    def __init__(self, parent = None):
        super().__init__(parent)

        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon(os.path.join(icons_path, "play_icon.svg")))
        self.play_button.setText("")
        self.play_button.setFlat(True)
        self.play_button.clicked.connect(self.handle_button_click)

        self.info_label = QLabel("Not Playing", alignment = Qt.AlignCenter)

        self.slider = QSlider(Qt.Orientation.Horizontal)

        self.elapsed_time_label = QLabel("0:00")
        self.total_time_label = QLabel("0:00")

        outer_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        seek_layout = QHBoxLayout()

        control_layout.addWidget(self.play_button)

        seek_layout.addWidget(self.elapsed_time_label)
        seek_layout.addWidget(self.slider)
        seek_layout.addWidget(self.total_time_label)

        outer_layout.addWidget(self.info_label)
        outer_layout.addLayout(control_layout)
        outer_layout.addLayout(seek_layout)

        self.setLayout(outer_layout)

    def handle_button_click(self):
        self.play_pause_signal.emit()

    def update_playback_icon(self, is_playing):
        if is_playing:
            self.play_button.setIcon(QIcon(os.path.join(icons_path, "pause_icon.svg")))
        else:
            self.play_button.setIcon(QIcon(os.path.join(icons_path, "play_icon.svg")))

    def update_playback_label(self, song, artist, feat_artists):
        if feat_artists != "NULL":
            self.info_label.setText(f"{artist} - {song} ft. {feat_artists}")
        else:
            self.info_label.setText(f"{artist} - {song}")

    def update_duration(self, duration):
        self.slider.setRange(0, duration)
        self.total_time_label.setText(self.format_time(duration))

    def update_position(self, position):
        self.slider.setValue(position)
        self.elapsed_time_label.setText(self.format_time(position))