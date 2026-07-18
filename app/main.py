from backend.scanner import scan_folder
from backend.extractor import extract_songs
from database import database
from ui import app
from ui.components import main_window, scan_folder_popup
from PySide6.QtCore import QTimer

application = app.App()

screen = application.primaryScreen()

window = main_window.MainWindow(screen)
window.showMaximized()

popup = scan_folder_popup.ScanPopup(window)
QTimer.singleShot(0, popup.show)

application.exec()

# folder = input("Enter folder location: ")
# songs = scan_folder(folder)
# songs_data = extract_songs(songs, folder)
# database.connection(songs_data)