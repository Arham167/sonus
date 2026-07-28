import os, time

def scan_folder(folder):
    songs = []
    for root, dirs, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() == ".mp3":
                songs.append(os.path.join(root, filename))
                time.sleep(0.001)

    return songs