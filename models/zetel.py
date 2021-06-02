from models.zaal import Zaal
from sqlite3 import Row


class Zetel:
    def __init__(self, id: int, zaal: Zaal, rij: int, nummer: int, toegankelijk: bool = False):
        self.id = id
        self.zaal = zaal
        self.rij = rij
        self.nummer = nummer
        self.toegankelijk = toegankelijk

    @property
    def rij(self):
        return self.rij

    @rij.setter
    def rij(self, rij):
        if rij < 1 or rij > self.zaal.rijen:
            raise ValueError
        self._rij = rij

    @property
    def nummer(self):
        return self.nummer

    @nummer.setter
    def nummer(self, nummer):
        if nummer < 1 or nummer > self.zaal.zetels_per_rij:
            raise ValueError
        self._nummer = nummer

    @classmethod
    def from_sql_row(cls, row: Row, prefix: str = ""):
        keys_zetel = ["id", "rij", "nummer", "toegankelijk"]
        zaal = Zaal.from_sql_row(row, "zaal_")
        data_zetel = {key: row[prefix+key] for key in keys_zetel}
        return cls(zaal=zaal, **data_zetel)


if __name__ == '__main__':
    pass
