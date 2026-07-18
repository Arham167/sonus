from PySide6.QtWidgets import QVBoxLayout, QDialog, QLabel
from PySide6.QtCore import QTimer

class ScanPopup(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Add Folder")

        self.label = QLabel("Enter folder path", self)
        self.label.show()
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showEvent(self, event):
        QTimer.singleShot(0, self.center_dialog)
        super().showEvent(event)

    def center_dialog(self):
        parent = self.parent()
        if parent is None:
            return

        top_level = parent.window() if parent.window() is not None else parent
        top_rect = top_level.frameGeometry()
        top_center_global = top_rect.center()

        popup_width = int(top_level.width() * 0.4)
        popup_height = int(top_level.height() * 0.3)
        self.setFixedSize(popup_width, popup_height)

        dlg_rect = self.frameGeometry()
        dlg_rect.moveCenter(top_center_global)
        self.move(dlg_rect.topLeft())