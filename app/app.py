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
    finished = Signal(int, int)
    error = Signal(str)

    def __init__(self, folder, mode = "background"):
        super().__init__()
        self.folder = folder
        self.mode = mode

    @Slot() # PySide6 Slot decorator

    def run(self):
        try:
            songs = scan_folder(self.folder)
            songs_data = extract_songs(songs, self.folder)

            if self.mode == "manual":
                database.initialize_database(songs_data)
                
                songs_count = database.get_songs_count()
                artists_count = database.get_artists_count()

                self.finished.emit(songs_count, artists_count)

            elif self.mode == "background":
                existing_paths = database.get_all_song_paths() 
                scanned_paths = []

                for song in songs_data:
                    scanned_path = song.get("path")
                    scanned_paths.append(scanned_path)

                existing_paths = [os.path.abspath(p) for p in existing_paths]
                scanned_paths = [os.path.abspath(p) for p in scanned_paths]

                new_paths = [path for path in scanned_paths if path not in existing_paths]
                removed_paths = [path for path in existing_paths if path not in scanned_paths]

                new_songs_data = [song for song in songs_data if os.path.abspath(song.get("path")) in new_paths]

                database.update_database(new_songs_data = new_songs_data, removed_paths = removed_paths)
                songs_count = database.get_songs_count()
                artists_count = database.get_artists_count()

                self.finished.emit(songs_count, artists_count)

        except Exception as e:
            self.error.emit(str(e))

class SonusApplication(QObject):
    def __init__(self):
        super().__init__()

        self.application = app.App()

        screen = self.application.primaryScreen()

        self.window = main_window.MainWindow(screen)
        self.window.artist_selected.connect(self.handle_artist_selection)
        self.window.showMaximized()

        folder = database.get_settings("music_folder")

        if folder and os.path.isdir(folder):
            self.background_scan(folder)

        else:
            self.popup = scan_folder_popup.ScanPopup(self.window)
            self.popup.scan_requested.connect(self.import_library)
            QTimer.singleShot(0, self.popup.show)

    def import_library(self, folder):
        self.popup.submit_button.setEnabled(False)
        self.popup.submit_button.setText("Scanning...")
        self.window.update_topbar(scanning = True)

        try:
            database.initialize_database(folder = folder)
            
        except Exception:
            self.popup.submit_button.setEnabled(True)
            self.popup.submit_button.setText("Submit")
            self.window.update_topbar(scanning = False)
            return

        self.scan_thread = QThread()
        self.scan_worker = ScanWorker(folder, mode = "manual")
        self.scan_worker.moveToThread(self.scan_thread)

        self.scan_thread.started.connect(self.scan_worker.run)
        self.scan_worker.finished.connect(self.on_import_finished)
        self.scan_worker.error.connect(self.on_import_error)
        self.scan_worker.finished.connect(self.scan_thread.quit)
        self.scan_worker.finished.connect(self.scan_worker.deleteLater)
        self.scan_thread.finished.connect(self.scan_thread.deleteLater)

        self.scan_thread.start()

    def background_scan(self, folder):
        self.window.update_topbar(scanning = True)
        
        self.scan_thread = QThread()
        self.scan_worker = ScanWorker(folder, mode = "background")
        self.scan_worker.moveToThread(self.scan_thread)

        self.scan_thread.started.connect(self.scan_worker.run)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.finished.connect(self.scan_thread.quit)
        self.scan_worker.finished.connect(self.scan_worker.deleteLater)
        self.scan_thread.finished.connect(self.scan_thread.deleteLater)

        self.scan_thread.start()

    def on_import_finished(self, songs_count, artists_count):
        self.popup.submit_button.setEnabled(True)
        self.popup.submit_button.setText("Submit")
        self.popup.close()

        self.window.update_topbar(songs_count, artists_count, scanning = False)
        self.get_artists_from_db()

    def on_import_error(self, message):
        self.popup.submit_button.setEnabled(True)
        self.popup.submit_button.setText("Submit")
        self.window.update_topbar(scanning = False)

    def on_scan_finished(self, songs_count, artists_count):
        self.window.update_topbar(songs_count, artists_count, scanning = False)
        self.get_artists_from_db()

    def get_artists_from_db(self):
        artists = database.list_all_artists()
        self.window.update_left_sidebar(artists)

    def handle_artist_selection(self, artist_id):
        if artist_id == "all":
            database.get_all_songs()
        else:
            rows = database.get_songs_from_artist(artist_id)
            artist = database.get_artist_from_id(artist_id)

            self.window.update_library_view(artist, rows)

    def run(self):
        self.application.exec()