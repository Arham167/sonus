# Main orchestrator

from database import database
from backend.scanner import scan_folder
from backend.extractor import extract_songs
from backend.playback import play_song, pause_song
from ui import app
from ui.components import main_window, scan_folder_popup, playback_bar
from PySide6.QtCore import QTimer, QThread, QObject, Signal, Slot, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
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
        self.window.song_selected.connect(self.handle_song_double_click)
        self.window.play_pause.connect(self.handle_playback)
        self.window.showMaximized()

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.playbackStateChanged.connect(self.on_playback_state_changed)
        self.player.durationChanged.connect(self.on_duration_changed)
        self.player.positionChanged.connect(self.on_position_changed)

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

        self.window.left_sidebar.artist_button.setEnabled(False)
        self.window.left_sidebar.playlist_button.setEnabled(False)

        try:
            database.initialize_database(folder = folder)
            
        except Exception:
            self.popup.submit_button.setEnabled(True)
            self.popup.submit_button.setText("Submit")
            self.window.left_sidebar.artist_button.setEnabled(True)
            self.window.left_sidebar.playlist_button.setEnabled(True)
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
        self.window.left_sidebar.artist_button.setEnabled(False)
        self.window.left_sidebar.playlist_button.setEnabled(False)
        
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

        self.window.left_sidebar.artist_button.setEnabled(True)
        self.window.left_sidebar.playlist_button.setEnabled(True)

        self.window.update_topbar(songs_count, artists_count, scanning = False)
        self.get_artists_from_db()

    def on_import_error(self, message):
        self.popup.submit_button.setEnabled(True)
        self.popup.submit_button.setText("Submit")
        
        self.window.left_sidebar.artist_button.setEnabled(True)
        self.window.left_sidebar.playlist_button.setEnabled(True)

        self.window.update_topbar(scanning = False)

    def on_scan_finished(self, songs_count, artists_count):
        self.window.update_topbar(songs_count, artists_count, scanning = False)
        self.window.left_sidebar.artist_button.setEnabled(True)
        self.window.left_sidebar.playlist_button.setEnabled(True)
        
        self.get_artists_from_db()

    def get_artists_from_db(self):
        artists = database.list_all_artists()
        self.window.update_left_sidebar(artists)

    def handle_artist_selection(self, artist_id):
        if artist_id == "all":
            songs = database.get_all_songs()
            artists = database.list_all_artists()
            self.window.update_library_view_all(artists, songs)
        else:
            songs = database.get_songs_from_artist(artist_id)
            artist = database.get_artist_from_id(artist_id)
            self.window.update_library_view_single(artist, songs)

    def handle_song_double_click(self, path):
        play_song(self.player, path)
        self.is_playing = True
        self.window.update_playback_state(self.is_playing)

        song, artist, feat_artists = database.get_song_and_artist_from_path(path)
        self.window.update_playback_label(song, artist, feat_artists)

        # self.window.update_seek_bar(1, self.player.durationChanged)

    def handle_playback(self):
        playing_state = QMediaPlayer.PlaybackState.PlayingState

        if self.player.playbackState() == playing_state:
            self.player.pause()
        elif self.player.source().isValid():
            self.player.play()

    def on_playback_state_changed(self, state):
        playing_state = QMediaPlayer.PlaybackState.PlayingState
        self.is_playing = state == playing_state
        self.window.update_playback_state(self.is_playing)

    def on_duration_changed(self, duration):
        self.window.update_seek_bar_duration(duration)

    def on_position_changed(self, position):
        self.window.update_seek_bar_position(position)

    def run(self):
        self.application.exec()