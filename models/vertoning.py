from dataclasses import dataclass
from models.film import Film
from models.zaal import Zaal
from sqlite3 import Row
from datetime import datetime


@dataclass
class Vertoning:
    datum: str
    film: Film
    zaal: Zaal
    drie_d: bool
    id: int = -1

    @classmethod
    def from_sql_row(cls, row: Row, prefix: str = ""):
        keys_vertoning = ["id", "datum", "drie_d"]
        keys_zaal = ["id", "nummer", "rijen",
                     "zetels_per_rij", "drie_d_ondersteuning"]
        keys_film = ["id", "imdb_id", "titel", "knt", "duur"]

        data_vertoning = {key: row[prefix+key] for key in keys_vertoning}
        data_film = {key: row["film_"+key] for key in keys_film}
        data_zaal = {key: row["zaal_"+key] for key in keys_zaal}

        return cls(film=Film(**data_film), zaal=Zaal(**data_zaal), **data_vertoning)

    @property
    def moment(self):
        datum = datetime.fromisoformat(self.datum)
        return datum.strftime("%H:%M")

    def __str__(self):
        return f"{'3D-' if self.drie_d else ''}Vertoning van {self.moment} in zaal {self.zaal}"


if __name__ == '__main__':
    pass
