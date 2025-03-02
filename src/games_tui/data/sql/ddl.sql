
-- Setup games table
CREATE TABLE IF NOT EXISTS games (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE COLLATE NOCASE
);

-- Setup achievements table
CREATE TABLE IF NOT EXISTS achievements (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    name    TEXT NOT NULL,
    desc    TEXT NOT NULL,

    FOREIGN KEY (game_id)
        REFERENCES games (id)
);

-- Setup user achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    achievement_id INTEGER NOT NULL,
    date           TIMESTAMP,

    FOREIGN KEY (achievement_id)
        REFERENCES achievements (id)
);

-- Table for highscores
CREATE TABLE IF NOT EXISTS highscores (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    date    TIMESTAMP NOT NULL,

    FOREIGN KEY (game_id)
        REFERENCES games (id) 
);

-- Setup rubik's highscores table
CREATE TABLE IF NOT EXISTS rubiks_scores (
    highscore_id INTEGER NOT NULL,
    moves        INTEGER NOT NULL,
    time_elapsed INTEGER NOT NULL,
    
    FOREIGN KEY (highscore_id)
        REFERENCES highscores (id)
);


-- Create games
INSERT INTO games (name)
VALUES (
    ('Chess'),
    ('Checkers'),
    ('Solitaire'),
    ('Rubiks')
);

-- Create achievements
INSERT INTO achievements (game_id, name, desc) 
VALUES (
    -- chess achievements:
    ( 
        (SELECT id FROM games WHERE name = 'Chess'), 
        'Checkmate in 10 Moves',
        'Win a game of chess 10 moves or less.'
    ),
    -- checkers achievements:
    (
        (SELECT id FROM games WHERE name = 'Chess'), 
        'King Me!',
        'Crown a piece by reaching the opponent’s last row'
    ),
    -- rubik's achievements
    (
        (SELECT id FROM games WHERE name = 'Rubiks'),
        '1 Minute Man',
        'Solve a rubiks cube in under 1 minute',
    )
); 
