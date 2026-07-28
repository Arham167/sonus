CREATE TABLE IF NOT EXISTS songs (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  channel TEXT NOT NULL,
                  artist TEXT NOT NULL
                  );

CREATE TABLE IF NOT EXISTS settings (
                  key TEXT PRIMARY KEY,
                  value TEXT NOT NULL
);