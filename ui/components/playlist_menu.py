from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout, QDialog, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import QTimer, Qt, Signal

class PlaylistMenu(QDialog):
    new_playlist = Signal(str, str)

    def __init__(self, song_path, parent = None):
        super().__init__(parent)
        self.song_path = song_path
        
        self.setWindowTitle("New Playlist")

        self.label = QLabel("Enter Playlist Name", self)

        self.input = QLineEdit(placeholderText = "...")
        self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.button = QPushButton("Create")
        self.button.clicked.connect(lambda checked = False: self.new_playlist.emit(self.song_path, self.input.text()))

        layout = QVBoxLayout(self)
        layout.addWidget(self.label, alignment = Qt.AlignCenter)
        layout.addStretch(1)

        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(self.input)
        row.addStretch(1)
        row.addWidget(self.button)
        row.addStretch(1)

        layout.addLayout(row)
        layout.addStretch(2)

    def center_dialog(self):
        parent = self.parent()
        if parent is None:
            return

        self.top_level = parent.window() if parent.window() is not None else parent
        top_rect = self.top_level.frameGeometry()
        top_center_global = top_rect.center()

        self.sizing()

        dlg_rect = self.frameGeometry()
        dlg_rect.moveCenter(top_center_global)
        self.move(dlg_rect.topLeft())

    def sizing(self):
        self.popup_width = int(self.top_level.width() * 0.4)
        self.popup_height = int(self.top_level.height() * 0.3)
        self.setFixedSize(self.popup_width, self.popup_height)

        self.input.setMinimumWidth(int(self.popup_width * 0.6))
        self.input.setMinimumHeight(int(self.popup_height * 0.2))

        self.button.setMinimumHeight(int(self.popup_height * 0.2))
