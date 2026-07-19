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
        QTimer.singleShot(0, self.popup.show)

    def run(self):
        self.application.exec()

# folder = input("Enter folder location: ")
# songs = scan_folder(folder)
# songs_data = extract_songs(songs, folder)
# database.connection(songs_data)