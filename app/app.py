from backend.scanner import scan_folder
from backend.extractor import extract_songs
from database import database
from ui import app
from ui.components import main_window, scan_folder_popup
from PySide6.QtCore import QTimer, QThread, QObject, Signal, Slot

class ScanWorker(QObject):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    @Slot()
    def run(self):
        try:
            songs = scan_folder(self.folder)
            songs_data = extract_songs(songs, self.folder)
            database.connection(songs_data)
            self.finished.emit(songs_data)
        except Exception as e:
            self.error.emit(str(e))

class SonusApplication():
    def __init__(self):
        self.application = app.App()

        screen = self.application.primaryScreen()

        self.window = main_window.MainWindow(screen)
        self.window.showMaximized()

        self.popup = scan_folder_popup.ScanPopup(self.window)
        self.popup.scan_requested.connect(self.import_library)
        QTimer.singleShot(0, self.popup.show)

    def import_library(self, folder):
        self.popup.submit_button.setEnabled(False)

        self.thread = QThread()
        self.worker = ScanWorker(folder)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_import_finished)
        self.worker.error.connect(self.on_import_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_import_finished(self, songs_data):
        self.popup.submit_button.setEnabled(True)

    def on_import_error(self, message):
        self.popup.submit_button.setEnabled(True)

    def run(self):
        self.application.exec()