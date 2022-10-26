-- NOC by order of abbreviation
SELECT abbreviation
FROM nocs
ORDER BY abbreviation ASC;

-- Jamaican Athletes Names, order last name if possible
SELECT DISTINCT athletes.name
FROM athletes, nocs, linkingtable
WHERE athletes.id = linkingtable.athlete_id
AND nocs.abbreviation = 'JAM'
AND nocs.id = linkingtable.noc_id;


-- Tyson Gray | Greg Lougnasis
-- Gold medals, Greg Lougnasis, sort year
SELECT athletes.name, nocs.abbreviation, events.event, medals.version, olympic_games.season, olympic_games.year
FROM athletes, nocs, events, medals, olympic_games, linkingtable               
where athletes.id = linkingtable.athlete_id
AND athletes.name ILIKE 'Greg%Louganis'
AND medals.id = linkingtable.medal_id
AND medals.version != 'NA'
AND events.id = linkingtable.event_id
AND olympic_games.id = linkingtable.olympic_game_id
AND nocs.id = linkingtable.noc_id
ORDER BY olympic_games.year;


-- List NOCS and nums gold medals won, decrease order by gold medals
SELECT nocs.abbreviation, COUNT(medals.version)
FROM nocs, medals, linkingtable
WHERE medals.id = linkingtable.medal_id
AND medals.version = 'Gold'
AND nocs.id = linkingtable.noc_id
GROUP BY nocs.abbreviation
ORDER BY COUNT(medals.version) DESC;


