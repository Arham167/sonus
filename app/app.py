# Main orchestrator

from database import database
from backend.scanner import scan_folder
from backend.extractor import extract_songs
from ui import app
from ui.components import main_window, scan_folder_popup
from PySide6.QtCore import QTimer, QThread, QObject, Signal, Slot
import os

# background worker for scanning folders

class ScanWorker(QObject):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    @Slot() # PySide6 Slot decorator

    def run(self):
        try:
            songs = scan_folder(self.folder)
            songs_data = extract_songs(songs, self.folder)
            database.initialize_database(songs_data)

            self.finished.emit(songs_data)

        except Exception as e:
            self.error.emit(str(e))

class SonusApplication(QObject):
    def __init__(self):
        super().__init__()

        self.application = app.App()

        screen = self.application.primaryScreen()

        self.window = main_window.MainWindow(screen)
        self.window.showMaximized()

        folder = database.get_settings("music_folder")

        if folder and os.path.isdir(folder):
            pass # (TODO: scan folder on each launch in background thread and update db if any existing thing changed or smth new added)

        else:
            self.popup = scan_folder_popup.ScanPopup(self.window)
            self.popup.scan_requested.connect(self.import_library)
            QTimer.singleShot(0, self.popup.show)

    def import_library(self, folder):
        self.popup.submit_button.setEnabled(False)
        self.popup.submit_button.setText("Scanning...")

        try:
            database.initialize_database(folder = folder)
            
        except Exception:
            self.popup.submit_button.setEnabled(True)
            self.popup.submit_button.setText("Submit")
            return

        self.scan_thread = QThread()
        self.scan_worker = ScanWorker(folder)
        self.scan_worker.moveToThread(self.scan_thread)

        self.scan_thread.started.connect(self.scan_worker.run)
        self.scan_worker.finished.connect(self.on_import_finished)
        self.scan_worker.error.connect(self.on_import_error)
        self.scan_worker.finished.connect(self.scan_thread.quit)
        self.scan_worker.finished.connect(self.scan_worker.deleteLater)
        self.scan_thread.finished.connect(self.scan_thread.deleteLater)

        self.scan_thread.start()

    def on_import_finished(self, songs_data):
        self.popup.submit_button.setEnabled(True)
        self.popup.submit_button.setText("Submit")
        self.popup.close()

    def on_import_error(self, message):
        self.popup.submit_button.setEnabled(True)
        self.popup.submit_button.setText("Submit")

    def run(self):
        self.application.exec()