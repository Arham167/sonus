from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, QEvent, Qt
from ui.components.top_bar import TopBar

class MainWindow(QMainWindow):
    def __init__(self, screen):
        super().__init__()
        self.setWindowTitle("Sonus")

        self.screen_geometry = screen.availableGeometry()
        _, _, width, height = self.screen_geometry.getRect()
        new_w = int(width * 0.9)
        new_h = int(height * 0.9)

        self.setMinimumSize(new_w, new_h)
        
        self.container = QWidget()

        outer_layout = QVBoxLayout(self.container)
        
        self.top_bar = TopBar()
        outer_layout.addWidget(self.top_bar)
        outer_layout.addStretch(1)

        self.setCentralWidget(self.container)

    def changeEvent(self, event):
        super().changeEvent(event)

        if event.type() != QEvent.WindowStateChange:
            return

        if event.oldState() & Qt.WindowMaximized and not self.isMaximized():
            size = self.size()
            center_x = self.screen_geometry.x() + (self.screen_geometry.width() - size.width()) // 2
            center_y = self.screen_geometry.y() + (self.screen_geometry.height() - size.height()) // 2
            self.move(center_x, center_y)

    def update_topbar(self, songs_count, artists_count):
        self.top_bar.update_counts(songs_count, artists_count)