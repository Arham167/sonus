import sqlite3, os, time, uuid

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "sonus.db")
schema_path = os.path.join(base_dir, "schema.sql")

def initialize_database(songs_data = None, folder = None):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            create_tables(cursor)

            if folder:
                insert_settings(cursor, key = "music_folder", value = folder)

            if songs_data:
                for song in songs_data:
                    name = song.get("name")
                    artist = song.get("artist")
                    path = song.get("path", "")
                    feat_artists = song.get("feat_artists", "NULL")

                    add_song(cursor, name, artist, feat_artists, path)

    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def update_database(folder = None, new_songs_data = None, removed_paths = None):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            create_tables(cursor)

            if folder:
                insert_settings(cursor, key = "music_folder", value = folder)

            if new_songs_data is not None and len(new_songs_data) > 0:
                for song in new_songs_data:
                    name = song.get("name")
                    artist = song.get("artist")
                    path = song.get("path", "")
                    feat_artists = song.get("feat_artists", "NULL")

                    add_song(cursor, name, artist, feat_artists, path)

            if removed_paths is not None and len(removed_paths) > 0:
                for path in removed_paths:
                        delete_song(cursor, path)

            return True

    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def create_tables(cursor):
    with open(schema_path) as f:
        cursor.executescript(f.read())

def add_song(cursor, name, artist, feat_artists, path):
    insert_song_statement = """INSERT INTO songs(song_id, name, artist, featuring_artists, path)
                                VALUES (?,?,?,?,?)"""
    song_id = song_exists(cursor, path)

    if not song_id:
        artist_id = add_artist(cursor, artist)
        song_id = str(uuid.uuid4())

        cursor.execute(insert_song_statement, (song_id, name, artist_id, feat_artists, path))

    else:
        print("already exists")

def add_artist(cursor, artist_name):
    insert_artist_statement = """INSERT INTO artists(artist_id, artist_name) 
                                 VALUES (?, ?)"""
    artist_id = artist_exists(cursor, artist_name)

    if not artist_id:
        artist_id = str(uuid.uuid4())
        cursor.execute(insert_artist_statement, (artist_id, artist_name))

        return artist_id

    else:
        return artist_id[0]

def song_exists(cursor, path):
    search_song_statement = """SELECT 1
                               FROM songs 
                               WHERE path = ?
                               LIMIT 1"""

    cursor.execute(search_song_statement, (path,))
    song_id = cursor.fetchone()

    if song_id is not None:
        return song_id

def artist_exists(cursor, artist_name):
    search_artist_statement = """SELECT artist_id 
                                 FROM artists 
                                 WHERE artist_name = ?"""

    cursor.execute(search_artist_statement, (artist_name,))
    artist_id = cursor.fetchone()

    if artist_id is not None:
        return artist_id

def delete_song(cursor, path):
    delete_statement = """DELETE FROM songs
                          WHERE path = ?"""
    cursor.execute(delete_statement, (path,))

def get_songs_count():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) AS TotalRows FROM songs")
            return cursor.fetchone()[0]
    
    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def get_artists_count():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) AS TotalRows FROM artists")
            return cursor.fetchone()[0]
    
    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def get_all_song_paths():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT path FROM songs")

            rows = cursor.fetchall()
            
            paths = []

            for row in rows:
                path = row[0]
                paths.append(path)

            return paths

    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def list_all_artists():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM artists")

            rows = cursor.fetchall()
            
            artists = []

            for row in rows:
                artists.append(row)

            return artists

    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def get_all_songs():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            get_statement = """SELECT * FROM songs"""

            cursor.execute(get_statement)
            rows = cursor.fetchall()

            return rows

    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def get_songs_from_artist(artist_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            get_statement = """SELECT * FROM songs WHERE artist = ?"""
            cursor.execute(get_statement, (artist_id,))
            rows = cursor.fetchall()

            return rows

    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def get_artist_from_id(artist_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            get_statement = """SELECT artist_name FROM artists WHERE artist_id = ?"""
            cursor.execute(get_statement, (artist_id,))
            artist = cursor.fetchone()

            return artist

    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

def insert_settings(cursor, key, value):
    create_tables(cursor)

    insert_statement = """INSERT INTO settings(key, value)
                          VALUES (?,?)
                          ON CONFLICT (key)
                          DO UPDATE SET value = excluded.value"""
    cursor.execute(insert_statement, (key, value))

def get_settings(key):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            create_tables(cursor)

            get_statement = """SELECT value
                            FROM settings
                            WHERE key = (?)"""
            cursor.execute(get_statement, (key,))

            row = cursor.fetchone()
            if row:
                return row[0]

            return None

    except sqlite3.OperationalError as e:
        print(f"Error happened: {e}")