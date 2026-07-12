import os

def extract_songs(songs, folder):
    songs_data = []

    for song in songs:
        relative_path = os.path.relpath(song, folder)
        split_name = relative_path.split(os.sep)

        if len(split_name) > 1:
            channel = split_name[0]
            name = split_name[-1]
            songs_data.append({
                "name": name,
                "channel": channel})

    return songs_data