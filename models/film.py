from dataclasses import dataclass
import requests
from configparser import ConfigParser


@dataclass
class Film:
    id: int
    titel: str
    duur: int
    imdb_id: str
    knt: bool = False
    drie_d: bool = False

    def __post_init__(self) -> None:
        self.beschrijving = ""
        self.poster_path = ""

    def is_lang(self) -> bool:
        return self.duur > 120

    def load_api_data(self) -> None:
        config = ConfigParser()
        config.read("config.ini")
        parameters = {
            "api_key": config["DEFAULT"]["API_KEY"],
            "external_source": "imdb_id",
            "language": "nl-NL"
        }
        try:
            data = requests.get(
                f"https://api.themoviedb.org/3/find/{self.imdb_id}", params=parameters).json()
        except:
            print("Fout bij ophalen filminformatie via API.")
        else:
            self.beschrijving = data["movie_results"][0]["overview"]
            self.poster_path = data["movie_results"][0]["poster_path"]

    def get_afbeelding(self, size: int = 0) -> str:
        if not self.poster_path:
            raise AttributeError(
                "Poster path niet beschikbaar. Vraag eerst informatie uit API.")

        return f"https://image.tmdb.org/t/p/{'original' if size == 0 else f'w{size}'}{self.poster_path}"

    def __str__(self):
        return self.titel

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Film):
            return NotImplemented
        return self.id == other.id


if __name__ == '__main__':
    # film = Film(id=1, titel="Frozen", duur=100, imdb_id="tt2294629")
    # film.load_api_data()
    # print(film.beschrijving)
    # print(film.get_afbeelding(300))
    pass
