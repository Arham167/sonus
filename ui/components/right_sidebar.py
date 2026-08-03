from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class RightSideBar(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.lyrics_label = QLabel("Lyrics")
        self.lyrics_label.setObjectName("leftSideBarHeading")

        layout = QVBoxLayout()
        layout.addWidget(self.lyrics_label, alignment = Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)