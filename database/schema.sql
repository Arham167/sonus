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