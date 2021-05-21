import PySimpleGUI as sg
from layouts.gui_utils import get_img_data
from models.film import Film


def create_layout_ticket(film: Film):
    return [
        [sg.HorizontalSeparator()],
        [
            sg.Image(data=get_img_data(film.get_afbeelding(),
                     maxsize=(200, 200), first=True)),
            sg.Text("Geniet van de film!",
                    font="Helvetica 40", text_color="white")
        ],
        [sg.HorizontalSeparator()]
    ]
