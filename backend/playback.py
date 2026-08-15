from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl

def play_song(player, path):
    player.setSource(QUrl.fromLocalFile(path))
    player.play()

def pause_song(player):
    player.pause()