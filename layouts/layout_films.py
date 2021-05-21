import PySimpleGUI as sg
from models.film import Film
from layouts.gui_utils import get_img_data


def create_layout_films(films: list[Film]):

    logo = sg.Image(data=get_img_data(
        "logo_wit.png", maxsize=(50, 50), first=True, local=True))

    rij_titel = [
        sg.Frame(title="", layout=[[logo, sg.Text("CINEMAX", font="Helvetica 30")]], pad=(0, 10))]

    FILMS_PER_RIJ = 5

    def maak_film_kolom(film: Film):
        return sg.Column([
            [sg.Image(data=get_img_data(film.get_afbeelding(),
                                        maxsize=(200, 250), first=True), k=f"film-{film.id}", enable_events=True)],
            [sg.Text(film.titel, font="Helvetica 18",
                     size=(20, 2), justification="center")]
        ], element_justification="center")

    def maak_film_rij(films: list[Film], start=0):
        return [maak_film_kolom(film) for film in films[start:start+FILMS_PER_RIJ]]

    film_rijen = [maak_film_rij(films, x)
                  for x in range(0, len(films), FILMS_PER_RIJ)]

    layout = [
        rij_titel,
        *film_rijen
    ]

    return layout
