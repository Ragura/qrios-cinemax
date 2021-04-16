-- SQLite

INSERT INTO films (titel, imdb_id, knt, drie_d, duur)
VALUES ("The Shawshank Redemption", "tt0111161", true, false, 142),
       ("The Godfather", "tt0068646", true, false, 175),
       ("The Hobbit", "tt0903624", false, true, 169),
       ("Inception", "tt1375666", false, false, 148),
       ("Spirited Away", "tt0245429", false, false, 125),
       ("Frozen", "tt2294629", false, true, 102),
       ("Saw 3D", "tt1477076", true, true, 90),
       ("Chaos Walking", "tt2076822", false, false, 109)
;       

INSERT INTO vertoningen (film_id, datum, zaal)
VALUES (1, date("now") || " 22:00:00+02:00", 1),
       (1, date("now", "+1 day") || " 22:00:00+02:00", 2),
       (2, date("now") || " 20:00:00+02:00", 2),
       (2, date("now") || " 22:00:00+02:00", 3),
       (3, date("now") || " 14:00:00+02:00", 1),
       (3, date("now") || " 17:00:00+02:00", 1),
       (3, date("now") || " 20:00:00+02:00", 4),
       (3, date("now", "+1 day") || " 14:00:00+02:00", 1),
       (3, date("now", "+1 day") || " 17:00:00+02:00", 1),
       (3, date("now", "+1 day") || " 20:00:00+02:00", 4),
       (4, date("now") || " 20:00:00+02:00", 5),
       (4, date("now", "+1 day") || " 20:00:00+02:00", 5),
       (5, date("now") || " 14:00:00+02:00", 5),
       (5, date("now") || " 17:00:00+02:00", 5),
       (6, date("now") || " 14:00:00+02:00", 4),
       (6, date("now") || " 17:00:00+02:00", 4),
       (5, date("now", "+1 day") || " 14:00:00+02:00", 5),
       (5, date("now", "+1 day") || " 17:00:00+02:00", 5),
       (6, date("now", "+1 day") || " 14:00:00+02:00", 4),
       (6, date("now", "+1 day") || " 17:00:00+02:00", 4),
       (7, date("now") || " 22:00:00+02:00", 6),
       (7, date("now", "+1 day") || " 22:00:00+02:00", 6)
;
