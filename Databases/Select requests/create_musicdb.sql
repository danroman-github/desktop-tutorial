/* Создание таблицы "жанры" */
CREATE TABLE IF NOT EXISTS genres (
    genres_id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

/* Создание таблицы "музыканты" */
CREATE TABLE IF NOT EXISTS musician (
    musician_id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    suname VARCHAR(128) NOT NULL
);

/* Создание таблицы "жанры и музыканты" */
CREATE TABLE IF NOT EXISTS genres_musician (
    genres_musician_id SERIAL PRIMARY KEY,
    genres_id INT NOT NULL REFERENCES genres(genres_id),
    musician_id INT NOT NULL REFERENCES musician(musician_id)
);

/* Создание таблицы "альбомы" */
CREATE TABLE IF NOT EXISTS albums (
    albums_id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    year VARCHAR(4) NOT NULL CHECK (year >= '1900' AND year <= '2100')  -- Ограничение на год
);

/* Создание таблицы "альбомы и музыканты" */
CREATE TABLE IF NOT EXISTS albums_musician (
    albums_musician_id SERIAL PRIMARY KEY,
    musician_id INT NOT NULL REFERENCES musician(musician_id),
    albums_id INT NOT NULL REFERENCES albums(albums_id)
);

/* Создание таблицы "треки" */
CREATE TABLE IF NOT EXISTS tracks (
    tracks_id SERIAL PRIMARY KEY,
    albums_id INT NOT NULL REFERENCES albums(albums_id),
    name VARCHAR(128) NOT NULL,
    duration INT NOT NULL CHECK (duration >= 0)  -- Ограничение на продолжительность трека
);

/* Создание таблицы "сборники" */
CREATE TABLE IF NOT EXISTS collection (
    collection_id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    year VARCHAR(4) NOT NULL CHECK (year >= '1900' AND year <= '2100')  -- Ограничение на год
);

/* Создание таблицы "треки и сборники" */
CREATE TABLE IF NOT EXISTS tracks_collection (
    tracks_collection_id SERIAL PRIMARY KEY,
    collection_id INT NOT NULL REFERENCES collection(collection_id),
    tracks_id INT NOT NULL REFERENCES tracks(tracks_id)
);