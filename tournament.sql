-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- Create the "players" table.  Players will be resgistered in this table.
-- The player_id IS automatically generated per player and IS unique.
CREATE TABLE players (
    player_id  serial PRIMARY KEY,
    name text
    );

-- Create the matches table.  Player 1 and Player 2 of each match will be
-- stored here.  The data in each colum will be the player's ID and refers
-- to the player_id column in the players table.
CREATE TABLE matches (
    match_id serial PRIMARY KEY,
    winner integer REFERENCES players (player_id) ON DELETE CASCADE,
    loser integer REFERENCES players (player_id) ON DELETE CASCADE,
    tied boolean
    );

-- Building....
CREATE VIEW standings AS
SELECT players.player_id, players.name,
       (coalesce(winners.win_points,0) + coalesce(ties.lose_points,0))
AS points, total.matches
FROM players
LEFT JOIN
(SELECT players.player_id, count(*) * 3
    AS win_points FROM players
    LEFT JOIN matches ON players.player_id = matches.winner
    WHERE tied IS False GROUP BY players.player_id) AS winners
    ON players.player_id = winners.player_id
LEFT JOIN
(SELECT players.player_id, count(*) * 1
    AS lose_points FROM players
    LEFT JOIN matches ON players.player_id = matches.winner
        or players.player_id = matches.loser
    WHERE tied IS True GROUP BY players.player_id) AS ties
    ON players.player_id = ties.player_id
LEFT JOIN
(SELECT players.player_id, count(matches)
    AS matches FROM players
    LEFT JOIN matches ON players.player_id = matches.winner
        or players.player_id = matches.loser
    GROUP BY players.player_id) AS total
    ON players.player_id = total.player_id
ORDER BY points DESC;
