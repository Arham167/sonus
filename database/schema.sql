-- songs table

CREATE TABLE IF NOT EXISTS songs (
                  song_id TEXT PRIMARY KEY NOT NULL,
                  name TEXT NOT NULL,
                  artist TEXT NOT NULL,
                  featuring_artists TEXT NOT NULL,
                  path TEXT NOT NULL
                  );

-- artists table

CREATE TABLE IF NOT EXISTS artists (
                  artist_id TEXT PRIMARY KEY NOT NULL,
                  artist_name TEXT NOT NULL UNIQUE
);

-- settings table

CREATE TABLE IF NOT EXISTS settings (
                  key TEXT PRIMARY KEY,
                  value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS playlists(
                  playlist_id text PRIMARY KEY NOT NULL,
                  name TEXT NOT NULL 
);

CREATE TABLE IF NOT EXISTS playlists_songs(
                  playlist_id text NOT NULL,
                  song_id text NOT NULL,

                  PRIMARY KEY (playlist_id, song_id),

                  FOREIGN KEY (playlist_id)
                    REFERENCES playlists(playlist_id)
                    ON DELETE CASCADE,

                  FOREIGN KEY (song_id)
                    REFERENCES songs(song_id)
                    ON DELETE CASCADE
);