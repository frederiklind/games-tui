SELECT h.id AS highscore_id, h.game_id, h.date, r.moves, r.time_elapsed
FROM highscores h
LEFT JOIN rubiks_scores r ON h.id = r.highscore_id
WHERE h.game_id = ?;
