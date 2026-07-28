from PySide6.QtCore import QXmlStreamNotationDeclaration
from PySide6 import QtWidgets
import sqlite3, os, time

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
                    name, channel = song.values()
                    artist = "NULL"

                    add_song(cursor, name, channel, artist)

                    time.sleep(0.001)

    except sqlite3.OperationalError as e:
        print(f"Error happened: {e}")

def create_tables(cursor):
    with open(schema_path) as f:
        cursor.executescript(f.read())

def add_song(cursor, name, channel, artist):
    insert_statement = """INSERT INTO songs(name, channel, artist)
                          VALUES (?,?,?)"""

    if not song_exists(cursor, name, channel):
        cursor.execute(insert_statement, (name, channel, artist))
        print("Added", name, "from", channel)

    else:
        pass

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