CREATE TABLE athletes (
    id SERIAL,
    name text
);

CREATE TABLE events (
    id SERIAL,
    event text
);

CREATE TABLE sports (
    id SERIAL,
    sport text
);

CREATE TABLE olympic_games (
    id SERIAL,
    year integer,
    season text,
    city text
);

CREATE TABLE medals(
    id SERIAL,
    version text
);

CREATE TABLE nocs (
    id SERIAL,
    abbreviation char(3)
);

CREATE TABLE linkingtable (
    athlete_id integer,
    noc_id integer,
    olympic_game_id integer,
    sport_id integer,
    event_id integer,
    medal_id integer,
    athlete_height float,
    athlete_weight float,
    athlete_age integer,
    athlete_sex char
);
