from dataclasses import dataclass
from models.vertoning import Vertoning
from models.film import Film
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlite3 import Row


@dataclass
class Ticket:
    vertoning: Vertoning
    minderjarig: bool
    prijs: float
    datum_verkoop: str = ""

    def __post_init__(self) -> None:
        self.datum_verkoop = self.datum_verkoop or str(
            datetime.now(tz=ZoneInfo("Europe/Brussels")))

    @staticmethod
    def bereken_prijs(vertoning: Vertoning, minderjarig: bool) -> float:
        prijs = 7 if minderjarig else 9
        if vertoning.drie_d:
            prijs += 1.5
        if vertoning.film.duur > 120:
            prijs += 1
        return prijs

    @classmethod
    def from_sql_row(cls, row: Row, prefix: str = ""):
        keys_ticket = ["minderjarig", "prijs", "datum_verkoop"]
        vertoning = Vertoning.from_sql_row(row, "vertoning_")
        data_ticket = {key: row[prefix+key] for key in keys_ticket}

        return cls(vertoning=vertoning, **data_ticket)

    def __iter__(self):
        return iter((self.datum_verkoop, self.vertoning.id, self.minderjarig, self.prijs))


if __name__ == '__main__':
    pass
