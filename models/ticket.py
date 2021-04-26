from dataclasses import dataclass
from models.vertoning import Vertoning
from models.film import Film
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class Ticket:
    vertoning: Vertoning
    minderjarig: bool

    def __post_init__(self) -> None:
        self.datum = str(datetime.now(tz=ZoneInfo("Europe/Brussels")))

    @property
    def prijs(self) -> float:
        return self.bereken_prijs(self.vertoning, self.minderjarig)

    @staticmethod
    def bereken_prijs(vertoning: Vertoning, minderjarig: bool) -> float:
        prijs = 7 if minderjarig else 9
        if vertoning.drie_d:
            prijs += 1.5
        if vertoning.film.duur > 120:
            prijs += 1
        return prijs

    def __iter__(self):
        return iter((self.datum, self.vertoning.id, self.minderjarig, self.prijs))


if __name__ == '__main__':
    pass
