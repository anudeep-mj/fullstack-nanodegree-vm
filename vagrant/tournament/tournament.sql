-- Initialize database

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- Table definitions for the tournament project.

-- Stores player info
CREATE TABLE playerlist (
id SERIAL NOT NULL,
name varchar,
PRIMARY KEY (id));

-- matchlist stores match info
CREATE TABLE matchlist (
id SERIAL NOT NULL,
winner INT REFERENCES playerlist(id) ON DELETE CASCADE,
loser INT REFERENCES playerlist(id) ON DELETE CASCADE,
PRIMARY KEY (id),
CHECK (winner <> loser)
);

-- winner_board holds the rankings of wins at any point of time
CREATE VIEW winner_board AS 
SELECT playerlist.id, playerlist.name, COUNT(matchlist.winner) AS wins 
FROM playerlist LEFT JOIN matchlist 
ON playerlist.id=matchlist.winner 
GROUP BY playerlist.id, playerlist.name 
ORDER BY wins desc;

-- total_matches has the information of total matches played and wins info for any team registered
CREATE VIEW total_matches AS 
select t.id, COUNT(m.winner+m.loser) AS totalmatches 
FROM playerlist AS t LEFT JOIN matchlist AS m 
ON t.id=m.winner or t.id=m.loser 
GROUP BY t.id 
ORDER BY totalmatches desc;

-- creating view for player standings
CREATE VIEW player_standings AS
SELECT total_matches.id, winner_board.name, winner_board.wins, total_matches.totalmatches 
FROM total_matches 
JOIN winner_board 
ON total_matches.id = winner_board.id;