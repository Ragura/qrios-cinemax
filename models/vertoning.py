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

    @classmethod
    def from_sql_row(cls, row: Row):
        # keys = ["id", "datum", "zaal"]
        film_data = {}
        vertoning_data = {}
        for key in row.keys():
            if key.startswith("film_"):
                film_data[key[5:]] = row[key]
            else:
                vertoning_data[key] = row[key]
        return cls(film=Film(**film_data), **vertoning_data)

    def __str__(self):
        return f"Vertoning van {self.datum.split(' ')[1][:-3]} in zaal {self.zaal}"


if __name__ == '__main__':
    pass
