from db.database import dbconn
from models.film import Film
from models.vertoning import Vertoning
from models.ticket import Ticket


def prefix_column_names_sql(table: str, prefix: str, *cols: str) -> str:
    '''Create SQL string to list column names with prefixed aliases'''
    return ", ".join([f"{table}.{col} as {prefix}_{col}" for col in cols])


class DataManager:

    @staticmethod
    def alle_films() -> list[Film]:
        with dbconn() as cur:
            cur.execute("SELECT * FROM films")
            return [Film(**row) for row in cur.fetchall()]

    @staticmethod
    def add_film(titel: str, duur: int, imdb_id: str, knt: bool) -> None:
        with dbconn() as cur:
            cur.execute("INSERT INTO films (titel, duur, imdb_id, knt) VALUES (?, ?, ?, ?)",
                        (titel, duur, imdb_id, knt))

    @staticmethod
    def zoek_films(titel: str = "", imdb_id: str = "", id: int = 0) -> list[Film]:
        with dbconn() as cur:
            query: list[str] = []
            params = []
            if titel:
                query.append("titel LIKE ?")
                params.append(f"%{titel}%")
            if imdb_id:
                query.append("imdb_id = ?")
                params.append(imdb_id)
            if id:
                query.append("id = ?")
                params.append(id)
            cur.execute(
                "SELECT * FROM films WHERE " + " OR ".join(query), params)
            return [Film(**row) for row in cur.fetchall()]

    @staticmethod
    def verwijder_film(id: int = 0) -> None:
        with dbconn() as cur:
            cur.execute(
                "DELETE FROM films WHERE id = ?", [id])

    # @staticmethod
    # def zoek_vertoning(film_id: int = 0) -> list[Vertoning]:
    #     with dbconn() as cur:
    #         cur.execute(
    #             "SELECT * FROM vertoningen WHERE film_id = ?", [film_id])
    #         return [Vertoning(**row) for row in cur.fetchall()]

    @staticmethod
    def zoek_vertoning_by_id(id: int) -> Vertoning:
        with dbconn() as cur:
            cur.execute(
                f"SELECT vertoningen.*, "
                + prefix_column_names_sql("films", "film",
                                          "id", "titel", "knt", "duur", "imdb_id")
                + f" FROM vertoningen "
                + f" INNER JOIN films ON vertoningen.film_id = films.id "
                + f"WHERE vertoningen.id = ?", [id])
            vertoning = Vertoning.from_sql_row(cur.fetchone())
            return vertoning

    @staticmethod
    def verwijder_vertoning(id: int = 0) -> None:
        with dbconn() as cur:
            cur.execute(
                "DELETE FROM vertoningen WHERE id = ?", [id])

    @staticmethod
    def add_vertoningen(vertoningen: list[dict]) -> None:
        vertoningen_lists = [list(vertoning.values())
                             for vertoning in vertoningen]
        with dbconn() as cur:
            cur.executemany("INSERT INTO vertoningen (film_id, datum, zaal, drie_d) VALUES (?, ?, ?, ?)",
                            vertoningen_lists)

    @staticmethod
    def tel_vertoningen(film_id: int = 0) -> int:
        with dbconn() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM vertoningen WHERE film_id = ?", [film_id])
            return cur.fetchone()[0]

    @staticmethod
    def vertoningen_vandaag() -> list[Vertoning]:
        with dbconn() as cur:
            cur.execute(
                f"SELECT vertoningen.*, "
                + prefix_column_names_sql("films", "film",
                                          "id", "titel", "knt", "duur", "imdb_id")
                + f" FROM vertoningen "
                f" INNER JOIN films ON vertoningen.film_id = films.id"
                f" WHERE DATE(vertoningen.datum) == DATE('now')")

            return [Vertoning.from_sql_row(row) for row in cur.fetchall()]

    @staticmethod
    def insert_tickets(tickets: list[Ticket]) -> None:
        with dbconn() as cur:
            t = [tuple(ticket) for ticket in tickets]
            cur.executemany(
                "INSERT INTO tickets (datum_verkoop, vertoning_id, minderjarig, prijs) VALUES (?, ?, ?, ?)", t)


if __name__ == '__main__':
    # print(DataManager.alle_films())
    # for vertoning in DataManager.vertoningen_vandaag():
    #     print(vertoning.film.titel)
    pass
