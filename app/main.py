import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.scanner import scan_folder
from app.extractor import extract_songs
from database import database

folder = input("Enter folder location: ")
songs = scan_folder(folder)
songs_data = extract_songs(songs, folder)
database.connection(songs_data)