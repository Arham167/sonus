import sqlite3, os

base_dir = os.getcwd()

def main():
    try:
        with sqlite3.connect("sonus.db") as conn:
            print("Opened SQLite database")
            cursor = conn.cursor()

            create_table(cursor)

            name = input("Enter song name: ")
            channel = input("Enter channel: ")
            artist = input("Enter artists (comma separated): ")

            add_song(cursor, name, channel, artist)

            list_all_songs(cursor)

            list_songs_from_artist(cursor, channel)

            conn.commit()

    except sqlite3.OperationalError as e:
        print(f"Error happened: {e}")

def create_table(cursor):
    with open(f"{base_dir}/schema.sql") as f:
        cursor.executescript(f.read())
        print("Created songs table")

def add_song(cursor, name, channel, artist):
    insert_statement = """INSERT INTO songs(name, channel, artist)
                          VALUES (?,?,?)"""

    if not song_exists(cursor, name, channel):
        cursor.execute(insert_statement, (name, channel, artist))
        print("Added")

    else:
        print("already exists")

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

if __name__ == "__main__":
    main()