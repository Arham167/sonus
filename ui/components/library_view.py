from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class LibraryView(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.library_label = QLabel("Library")
        self.library_label.setObjectName("leftSideBarHeading")

        layout = QVBoxLayout()
        layout.addWidget(self.library_label, alignment = Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)