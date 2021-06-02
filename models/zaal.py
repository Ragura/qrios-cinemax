from dataclasses import dataclass
from sqlite3 import Row


@dataclass
class Zaal:
    id: int
    nummer: int
    rijen: int
    zetels_per_rij: int
    drie_d_ondersteuning: bool = False

    @classmethod
    def from_sql_row(cls, row: Row, prefix: str = ""):
        keys_zaal = ["id", "nummer", "drie_d_ondersteuning",
                     "rijen", "zetels_per_rij"]
        data_zaal = {key: row[prefix+key] for key in keys_zaal}
        return cls(**data_zaal)


if __name__ == '__main__':
    pass
