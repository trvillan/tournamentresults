-- File: tournament.sql
-- Author: Tyler Villanueva
-- Date: Oct 19, 2016
-- Rev 1

-- Rev History:
-- rev - date - author - notes
-- 0 - Oct 19, 2016 - Tyler Villanueva/Udiactiy - Initial design
-- 1 - Oct 20, 2019 - Tyler Villanueva - Re-design

-- To initialize:
-- createdb tournament
-- psql tournament

-- Create the table that will hold all players.
CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	p_name TEXT NOT NULL
);

-- Create the table that will hold all match results.
-- Each match will have 2 results.  One for the loser and one for the winner.
CREATE TABLE results (
	id integer REFERENCES players (id),
	opponent integer REFERENCES players (id),  
	result boolean NOT NULL,
	PRIMARY KEY (id, opponent)
);

-- Create a view that will be used to return player rankings.
CREATE VIEW standings as
	SELECT players.id, players.p_name,
		Count(nullif(results.result, false)) AS wins,
        Count(results.id) AS matches
    FROM players LEFT JOIN results ON players.id = results.id
    GROUP BY players.id ORDER BY wins desc;

-- Uncomment to kill tables and views.
-- drop table players CASCADE;

-- Uncomment to list all custom views for this DB.
-- select table_name from INFORMATION_SCHEMA.views WHERE table_schema = ANY (current_schemas(false));
