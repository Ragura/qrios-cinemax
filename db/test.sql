-- SQLite
-- SELECT tickets.*, 
--        vertoningen.id as vertoning_id,
--        vertoningen.film_id as vertoning_film_id,
--        vertoningen.datum as vertoning_datum,
--        vertoningen.zaal as vertoning_zaal,
--        vertoningen.drie_d as vertoning_drie_d,
--        films.imdb_id as film_imdb_id,
--        films.titel as film_titel,
--        films.knt as film_knt,
--        films.duur as film_duur
-- FROM tickets
-- INNER JOIN vertoningen ON tickets.vertoning_id = vertoningen.id
-- INNER JOIN films ON vertoningen.film_id = films.id
-- WHERE tickets.datum_verkoop BETWEEN "2021-05-10 17:00:00+02:00" AND "2021-05-11" 

SELECT  
       films.titel as film_titel,
       SUM(tickets.prijs) as omzet
FROM tickets  
INNER JOIN vertoningen ON tickets.vertoning_id = vertoningen.id
INNER JOIN films ON vertoningen.film_id = films.id
GROUP BY films.id
ORDER BY omzet DESC
;