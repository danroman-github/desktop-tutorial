/* Название и продолжительность самого длительного трека */
SELECT name, duration
FROM tracks
ORDER BY duration DESC
LIMIT 1;

/* Название треков продолжительностью не менее 3,5 минут */
SELECT name
FROM tracks
WHERE duration >= 210;

/* Названия сборников, вышедших в период с 2018 по 2020 год включительно */
SELECT name
FROM collection
WHERE year BETWEEN '2018' AND '2020';

/* Исполнители, чьё имя состоит из одного слова */
SELECT name, suname
FROM musician
WHERE name NOT LIKE '% %';

/* Название треков, которые содержат слово «мой» или «my» */
SELECT name
FROM tracks
WHERE name LIKE '%мой%' OR name LIKE '%my%';

/* Количество исполнителей в каждом жанре */
SELECT g.name AS genre, COUNT(gm.musician_id) AS musician_count
FROM genres AS g
LEFT JOIN genres_musician AS gm ON g.genres_id = gm.genres_id
GROUP BY g.name;

/* Количество треков, вошедших в альбомы 2019–2020 годов */
SELECT COUNT(t.tracks_id) AS track_count
FROM tracks AS t
JOIN albums AS a ON t.albums_id = a.albums_id
WHERE a.year BETWEEN '2019' AND '2020';

/* Средняя продолжительность треков по каждому альбому */
SELECT a.name AS album_name, AVG(t.duration) AS average_duration
FROM albums AS a
JOIN tracks AS t ON a.albums_id = t.albums_id
GROUP BY a.name;

/* Все исполнители, которые не выпустили альбомы в 2020 году */
SELECT DISTINCT m.name, m.suname
FROM musician AS m
WHERE m.musician_id NOT IN (
    SELECT am.musician_id
    FROM albums_musician AS am
    JOIN albums AS a ON am.albums_id = a.albums_id
    WHERE a.year = '2020'
);

/* Названия сборников, в которых присутствует конкретный исполнитель (Вячеслав) */
SELECT DISTINCT c.name AS collection_name
FROM collection AS c
JOIN tracks_collection AS tc ON c.collection_id = tc.collection_id
JOIN tracks AS t ON tc.tracks_id = t.tracks_id
JOIN albums_musician AS am ON t.albums_id = am.albums_id
JOIN musician AS m ON am.musician_id = m.musician_id
WHERE m.name = 'Вячеслав';

/* Названия альбомов, в которых присутствуют исполнители более чем одного жанра */
SELECT a.name AS album_name
FROM albums AS a
JOIN albums_musician AS am ON a.albums_id = am.albums_id
JOIN genres_musician AS gm ON am.musician_id = gm.musician_id
GROUP BY a.albums_id, a.name
HAVING COUNT(DISTINCT gm.genres_id) > 1;

/* Наименования треков, которые не входят в сборники */
SELECT t.name AS track_name
FROM tracks AS t
LEFT JOIN tracks_collection AS tc ON t.tracks_id = tc.tracks_id
WHERE tc.tracks_id IS NULL;

/* Исполнитель или исполнители, написавшие самый короткий по продолжительности трек */
SELECT DISTINCT m.name, m.suname
FROM musician AS m
JOIN albums_musician AS am ON m.musician_id = am.musician_id
JOIN tracks AS tr ON am.albums_id = tr.albums_id
WHERE tr.duration = (SELECT MIN(duration) FROM tracks);
    
/* Названия альбомов, содержащих наименьшее количество треков */
SELECT a.name AS album_name
FROM albums AS a
JOIN tracks AS t ON a.albums_id = t.albums_id
GROUP BY a.albums_id, a.name
HAVING COUNT(t.tracks_id) = (
    SELECT MIN(track_count)
    FROM (
        SELECT COUNT(tracks_id) AS track_count
        FROM tracks
        GROUP BY albums_id
    ) AS subquery
);


