from dataclasses import dataclass
from models.film import Film
from sqlite3 import Row
from datetime import datetime


@dataclass
class Vertoning:
    id: int
    datum: str
    film: Film
    zaal: int
    drie_d: bool

    @classmethod
    def from_sql_row(cls, row: Row, prefix: str = ""):
        keys_vertoning = ["id", "datum", "zaal", "drie_d"]
        keys_film = ["id", "imdb_id", "titel", "knt", "duur"]

        data_vertoning = {key: row[prefix+key] for key in keys_vertoning}
        data_film = {key: row["film_"+key] for key in keys_film}

        return cls(film=Film(**data_film), **data_vertoning)

    @property
    def moment(self):
        datum = datetime.fromisoformat(self.datum)
        return datum.strftime("%H:%M")

    def __str__(self):
        return f"{'3D-' if self.drie_d else ''}Vertoning van {self.moment} in zaal {self.zaal}"


if __name__ == '__main__':
    pass
