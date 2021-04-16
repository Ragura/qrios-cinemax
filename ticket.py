from dataclasses import dataclass
from vertoning import Vertoning
from film import Film
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
        return self.bereken_prijs(self.vertoning.film, self.minderjarig)

    @staticmethod
    def bereken_prijs(film: Film, minderjarig: bool) -> float:
        prijs = 7 if minderjarig else 9
        if film.drie_d:
            prijs += 1.5
        if film.duur > 120:
            prijs += 1
        return prijs

    def __iter__(self):
        return iter((self.datum, self.vertoning.id, self.minderjarig, self.prijs))


if __name__ == '__main__':
    pass
