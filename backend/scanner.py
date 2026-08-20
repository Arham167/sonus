import os, time

def scan_folder(folder):
    allowed_extensions = [".mp3", ]
    songs = []
    for root, _, filenames in os.walk(folder):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in allowed_extensions:
                songs.append(os.path.join(root, filename))
                time.sleep(0.001)

    return songs