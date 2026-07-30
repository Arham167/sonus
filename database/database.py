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
                    channel = song.get("channel")
                    path = song.get("path", "")
                    artist = song.get("artist", "NULL")

                    add_song(cursor, name, channel, artist, path)

                    time.sleep(0.001)

    except sqlite3.OperationalError as e:
        print(f"Error happened: {e}")

def create_tables(cursor):
    with open(schema_path) as f:
        cursor.executescript(f.read())

def add_artist(cursor, artist_name):
    print("adding artist")

    cursor.execute(
        "SELECT artist_id FROM artists WHERE artist_name = ?",
        (artist_name,),)

    artist_exists = cursor.fetchone()

    if artist_exists:
        return artist_exists[0]

    else:
        artist_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO artists(artist_id, artist_name) VALUES (?, ?)",
            (artist_id, artist_name),
        )
        print("added artist")
        return artist_id 

def add_song(cursor, name, channel, artist, path):
    insert_statement = """INSERT INTO songs(song_id, name, channel, artist, path)
                          VALUES (?,?,?,?,?)"""

    if not song_exists(cursor, name, channel):
        artist_id = add_artist(cursor, channel)
        song_id = str(uuid.uuid4())

        cursor.execute(insert_statement, (song_id, name, artist_id, artist, path))
        print("Added", name, "from", channel)

    else:
        print("error")

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

def song_exists(cursor, name, channel):
    search_song_statement = """SELECT 1
                               FROM songs 
                               WHERE name = ?
                               AND channel = ?
                               LIMIT 1"""

    cursor.execute(search_song_statement, (name, channel))
    rows = cursor.fetchall()

    if len(rows) > 0:
        return True

def list_all_songs(cursor):
    list_statement = """SELECT *
                        FROM songs"""

    cursor.execute(list_statement)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

def list_songs_from_artist(cursor, channel):
    list_statement = """SELECT *
                        FROM songs
                        WHERE channel = ?"""
    
    cursor.execute(list_statement, (channel,))
    rows = cursor.fetchall()

    for row in rows:
        print(row)