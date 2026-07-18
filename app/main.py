import os, sys
from PySide6.QtWidgets import QApplication

from backend.scanner import scan_folder
from backend.extractor import extract_songs
from database import database
from ui import app
from ui.components import main_window

application = app.App()
window = main_window.MainWindow()
window.showMaximized()
application.exec()

# folder = input("Enter folder location: ")
# songs = scan_folder(folder)
# songs_data = extract_songs(songs, folder)
# database.connection(songs_data)