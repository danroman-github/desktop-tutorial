/* Заполнение таблицы "жанры" */
INSERT INTO genres (name) 
VALUES 
	('pop'),
	('rock'),
	('jazz');

/* Заполнение таблицы "музыканты" */
INSERT INTO musician (name, suname) 
VALUES 
	('Bruno', 'Mars'),
	('Вячеслав', 'Бутусов'),
	('Frank', 'Sinatra'),
	('Louis', 'Armstrong');
	
/* Заполнение таблицы "жанры и музыканты" */
INSERT INTO genres_musician (genres_id, musician_id) 
VALUES 
	(1, 1), 
	(2, 2), 
	(1, 3), 
	(3, 3),
	(3, 4);

/* Заполнение таблицы "альбомы" */
INSERT INTO albums (name, year) 
VALUES 
	('24K Magic', 2010),
	('Гудбай, Америка!', 2017),
	('A Jolly Christmas', 1999),
	('Christmas with Louis Armstrong', 1997);
	
/* Заполнение таблицы "альбомы и музыканты" */
INSERT INTO albums_musician (musician_id, albums_id) 
VALUES 
	(1, 1), 
	(2, 2), 
	(3, 3), 
	(4, 4);
	
/* Заполнение таблицы "треки" */
INSERT INTO tracks (albums_id, name, duration) 
VALUES 
	(1, '24K Magic', 225),
	(1, 'Chunky', 186),
	(1, 'Finesse', 189),
	(1, 'Perm', 210),
	(1, 'Versace on the Floor', 261),
	(1, 'Too Good to Say Goodbye', 281),
	(2, 'Люди', 292),
	(2, 'Intro', 26),
	(2, 'Синоптики', 283),
	(2, 'Я хочу быть с тобой', 329),
	(2, 'Бриллиантовые дороги', 322),
	(3, 'Jingle Bells', 120),
	(3, 'Mistletoe And Holly', 138),
	(3, 'The Christmas Waltz', 183),
	(3, 'The First Noel', 164),
	(3, 'Adeste Fideles', 154),
	(4, 'Cool Yule', 172),
	(4, 'Christmas in New Orleans', 171),
	(4, 'Winter Wonderland', 176),
	(4, 'Moments To Remember', 187);

/* Заполнение таблицы "сборники" */
INSERT INTO collection (name, year) 
VALUES 
	('Christmas', 2011),
	('Сборник 2018', 2018),
	('Лучшее 2018', 2018),
	('В дорогу', 2019);

/* Заполнение таблицы "треки и сборники" */
INSERT INTO tracks_collection (collection_id, tracks_id) 
VALUES 
	(1, 12), 
	(1, 14), 
	(1, 17), 
	(1, 19),
	(2, 14),
	(2, 7),
	(2, 15),
	(2, 17),
	(3, 1),
	(3, 4),
	(3, 15),
	(3, 17),
	(3, 5),
	(4, 8),
	(4, 9),
	(4, 3),
	(4, 14),
	(4, 11);
