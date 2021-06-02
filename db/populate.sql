-- SQLite

INSERT INTO films (titel, imdb_id, knt, duur)
VALUES ("The Shawshank Redemption", "tt0111161", true, 142),
       ("The Godfather", "tt0068646", true, 175),
       ("The Hobbit", "tt0903624", false, 169),
       ("Inception", "tt1375666", false, 148),
       ("Spirited Away", "tt0245429", false, 125),
       ("Frozen", "tt2294629", false, 102),
       ("Saw 3D", "tt1477076", true, 90),
       ("Chaos Walking", "tt2076822", false, 109)
;  

INSERT INTO zalen (nummer, drie_d_ondersteuning, rijen, zetels_per_rij)
VALUES (1, true, 10, 15),
       (2, true, 12, 12),
       (3, true, 14, 10),
       (4, false, 14, 13),
       (5, false, 10, 15),
       (6, false, 10, 13),
       (7, false, 6, 11)
;

INSERT INTO vertoningen (film_id, datum, zaal_id, drie_d)
VALUES (1, date("now") || " 22:00:00+02:00", 1, false),
       (1, date("now", "+1 day") || " 22:00:00+02:00", 2, false),
       (2, date("now") || " 20:00:00+02:00", 2, false),
       (2, date("now") || " 22:00:00+02:00", 3, false),
       (3, date("now") || " 14:00:00+02:00", 1, true),
       (3, date("now") || " 17:00:00+02:00", 1, true),
       (3, date("now") || " 20:00:00+02:00", 4, false),
       (3, date("now", "+1 day") || " 14:00:00+02:00", 1, true),
       (3, date("now", "+1 day") || " 17:00:00+02:00", 1, true),
       (3, date("now", "+1 day") || " 20:00:00+02:00", 4, false),
       (4, date("now") || " 20:00:00+02:00", 5, false),
       (4, date("now", "+1 day") || " 20:00:00+02:00", 5, false),
       (5, date("now") || " 14:00:00+02:00", 5, true),
       (5, date("now") || " 17:00:00+02:00", 5, true),
       (6, date("now") || " 14:00:00+02:00", 4, true),
       (6, date("now") || " 17:00:00+02:00", 4, true),
       (5, date("now", "+1 day") || " 14:00:00+02:00", 5, true),
       (5, date("now", "+1 day") || " 17:00:00+02:00", 5, true),
       (6, date("now", "+1 day") || " 14:00:00+02:00", 4, true),
       (6, date("now", "+1 day") || " 17:00:00+02:00", 4, true),
       (7, date("now") || " 22:00:00+02:00", 6, false),
       (7, date("now", "+1 day") || " 22:00:00+02:00", 6, false)
;

-- INSERT INTO tickets (datum_verkoop, vertoning_id, minderjarig, prijs)
-- VALUES (date("now") || " 13:22:00+02:00", 1, false, 11),
--        (date("now") || " 21:33:00+02:00", 4, false, 13)
-- ;
       