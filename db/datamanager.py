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
    def vertoningen_vandaag() -> list[Vertoning]:
        with dbconn() as cur:
            cur.execute(
                f"SELECT vertoningen.*, "
                + prefix_column_names_sql("films", "film",
                                          "id", "titel", "knt", "duur", "drie_d", "imdb_id")
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
