from backend.scanner import scan_folder
from backend.extractor import extract_songs
from database import database
from ui import app
from ui.components import main_window, scan_folder_popup
from PySide6.QtCore import QTimer

class SonusApplication():
    def __init__(self):
        self.application = app.App()

        screen = self.application.primaryScreen()

        self.window = main_window.MainWindow(screen)
        self.window.showMaximized()

        self.popup = scan_folder_popup.ScanPopup(self.window)
        self.popup.scan_requested.connect(self.scan)
        QTimer.singleShot(0, self.popup.show)

    def scan(self, folder):
        songs = scan_folder(folder)
        self.extract(songs, folder)

    def extract(self, songs, folder):
        songs_data = extract_songs(songs, folder)
        self.add(songs_data)

    def add(self, songs_data):
        database.connection(songs_data)

    def run(self):
        self.application.exec()

# folder = input("Enter folder location: ")
# songs = scan_folder(folder)
# songs_data = extract_songs(songs, folder)
# database.connection(songs_data)