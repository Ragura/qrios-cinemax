import PySimpleGUI as sg
import locale
from layouts.gui_utils import get_img_data

from db.datamanager import DataManager as dm
from models.film import Film
from models.vertoning import Vertoning
from models.ticket import Ticket

from typing import Optional


locale.setlocale(locale.LC_ALL, "")
sg.theme('DarkBlue4')

vertoningen_vandaag = dm.vertoningen_vandaag()
films = list({vertoning.film for vertoning in vertoningen_vandaag})

logo = sg.Image(data=get_img_data(
    "logo_wit.png", maxsize=(50, 50), first=True, local=True))

kolom_links = [
    [sg.Listbox(values=films, k="-FILMS-", enable_events=True, size=(30, 14))]
]

kolom_rechts = [
    [sg.Text("Vertoningen")],
    [sg.Listbox(values=[], k="-VERTONINGEN-",
                size=(30, 5), enable_events=True)],
    [
        sg.Column([
            [
                sg.Text("Aantal volwassenen ", size=(20, 1)),
                sg.Spin(values=[i for i in range(
                    999)], enable_events=True, key="-VOLWASSENEN-", size=(2, 1))
            ]
        ])
    ],
    [
        sg.Column([
            [
                sg.Text("Aantal kinderen: ", size=(20, 1)),
                sg.Spin(values=[i for i in range(
                    999)], enable_events=True, key="-KINDEREN-", size=(2, 1))
            ]
        ], k="-RIJ_KINDEREN-")
    ],
    [
        sg.Text("Prijs:", size=(20, 1)),
        sg.Text("", k="-PRIJS-", size=(8, 1))
    ],
    [
        sg.Button("Tickets kopen", k="-KOPEN-", disabled=True)
    ]
]

layout = [
    [sg.Frame(title="", layout=[
        [logo, sg.Text("CINEMAX", font="Helvetica 30")]], pad=(0, 20))],
    [sg.Column(kolom_links), sg.Column(kolom_rechts)]
]

global window
window = sg.Window('Cinemax', layout, size=(
    640, 480), element_justification="center", font="Helvetica 16", element_padding=(5, 5))


def update_prijs(vertoning: Vertoning) -> None:
    aantal_volwassenen = int(window["-VOLWASSENEN-"].get())
    aantal_kinderen = int(window["-KINDEREN-"].get())

    prijs = 0
    if aantal_volwassenen:
        prijs += Ticket.bereken_prijs(vertoning, False) * aantal_volwassenen
    if aantal_kinderen:
        prijs += Ticket.bereken_prijs(vertoning, True) * aantal_kinderen

    window["-PRIJS-"].update(value=locale.currency(prijs))
    if prijs > 0:
        window["-KOPEN-"].update(disabled=False)
    else:
        window["-KOPEN-"].update(disabled=True)


huidige_film: Optional[Film] = None
huidige_vertoning: Optional[Vertoning] = None

while True:
    event, values = window.read() or (None, None)
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == "-FILMS-":
        huidige_film = values["-FILMS-"][0]
        huidige_vertoning = None
        vertoningen = [
            vertoning for vertoning in vertoningen_vandaag if vertoning.film == huidige_film]
        window["-VERTONINGEN-"].update(values=vertoningen)

        window["-KINDEREN-"].update(value=0)
        window["-VOLWASSENEN-"].update(value=0)
        window["-PRIJS-"].update("")

    if event == "-VERTONINGEN-":
        huidige_vertoning = values["-VERTONINGEN-"][0]
        if huidige_vertoning:
            update_prijs(huidige_vertoning)

    if event == "-KINDEREN-" or event == "-VOLWASSENEN-":
        if huidige_vertoning:
            update_prijs(huidige_vertoning)

    if event == "-KOPEN-":
        if (huidige_vertoning):
            aantal_volwassenen = int(values["-VOLWASSENEN-"])
            aantal_kinderen = int(values["-KINDEREN-"])
            prijs_volwassene = Ticket.bereken_prijs(huidige_vertoning, False)
            prijs_kind = Ticket.bereken_prijs(huidige_vertoning, True)
            tickets = [Ticket(huidige_vertoning, True, prijs_kind) for _ in range(
                aantal_kinderen)] + [Ticket(huidige_vertoning, False, prijs_volwassene) for _ in range(aantal_volwassenen)]
            dm.insert_tickets(tickets)
            huidige_film = None
            huidige_vertoning = None
            window["-FILMS-"].update(set_to_index=-1)
            window["-VERTONINGEN-"].update(set_to_index=-1)
            window["-KINDEREN-"].update(value=0)
            window["-VOLWASSENEN-"].update(value=0)
            window["-PRIJS-"].update(value="")
