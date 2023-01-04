PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS games_played;
CREATE TABLE games_played (
        game_number  INTEGER PRIMARY KEY AUTOINCREMENT,
        score INT NOT NULL
    );

DROP TABLE IF EXISTS scorebord;
CREATE TABLE scorebord (
        name TEXT NOT NULL,
        score INT NOT NULL
    );