CREATE TABLE IF NOT EXISTS songs (
                  song_id TEXT PRIMARY KEY NOT NULL,
                  name TEXT NOT NULL,
                  channel TEXT NOT NULL,
                  artist TEXT NOT NULL,
                  path TEXT NOT NULL
                  );

CREATE TABLE IF NOT EXISTS artists (
                  artist_id TEXT PRIMARY KEY NOT NULL,
                  artist_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS settings (
                  key TEXT PRIMARY KEY,
                  value TEXT NOT NULL
);