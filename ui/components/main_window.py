from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer, QEvent, Qt

class MainWindow(QMainWindow):
    def __init__(self, screen):
        super().__init__()
        self.setWindowTitle("Sonus")

        self.geometry = screen.availableGeometry()
        _, _, width, height = self.geometry.getRect()
        new_w = int(width * 0.9)
        new_h = int(height * 0.9)

        self.setMinimumSize(new_w, new_h)

    def changeEvent(self, event):
        super().changeEvent(event)

        if event.type() != QEvent.WindowStateChange:
            return

        if event.oldState() & Qt.WindowMaximized and not self.isMaximized():
            size = self.size()
            center_x = self.geometry.x() + (self.geometry.width() - size.width()) // 2
            center_y = self.geometry.y() + (self.geometry.height() - size.height()) // 2
            self.move(center_x, center_y)