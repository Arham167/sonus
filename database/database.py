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
                print("have data")
                for song in songs_data:
                    name = song.get("name")
                    artist = song.get("artist")
                    path = song.get("path", "")
                    feat_artists = song.get("feat_artists", "NULL")

                    add_song(cursor, name, artist, feat_artists, path)

                    time.sleep(0.001)

    except sqlite3.OperationalError as e:
        print(f"error happened: {e}")

# read schema and create DB tables
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
        print("Added", name, "from", artist)

    else:
        print("error")

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

def insert_settings(cursor, key, value):
    insert_statement = """INSERT INTO settings(key, value)
                          VALUES (?, ?)
                          ON CONFLICT (key)
                          DO UPDATE SET value = excluded.value"""
    cursor.execute(insert_statement, (key, value))

def get_settings(key):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

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

def list_all_songs(cursor):
    list_statement = """SELECT *
                        FROM songs"""

    cursor.execute(list_statement)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def list_songs_from_artist(cursor, artist):
    list_statement = """SELECT *
                        FROM songs
                        WHERE artist = ?"""
    
    cursor.execute(list_statement, (artist,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)