from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout, QDialog, QLabel, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import QTimer, Qt, Signal

class ScanPopup(QDialog):
    scan_requested = Signal(str)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Add Folder")

        self.label = QLabel("Enter folder path", self)

        self.input = QLineEdit(placeholderText = "Folder Path")
        self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.scan)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label, alignment = Qt.AlignCenter)
        layout.addStretch(1)

        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(self.input)
        row.addStretch(1)
        row.addWidget(self.browse_button)
        row.addStretch(1)

        layout.addLayout(row)
        layout.addStretch(2)
        layout.addWidget(self.submit_button, alignment = Qt.AlignCenter)

        self.setLayout(layout)

    def showEvent(self, event):
        QTimer.singleShot(0, self.center_dialog)
        super().showEvent(event)

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

        self.browse_button.setMinimumHeight(int(self.popup_height * 0.2))

    def browse(self):
        path = QFileDialog.getExistingDirectory()
        if path:
            self.input.setText(path)

    def scan(self):
        path = self.input.text().strip()
        if not path:
            return

        self.scan_requested.emit(path)
        self.close()