import PySimpleGUI as sg

from layouts.layout_films import create_layout_films
from layouts.layout_detail import create_layout_detail, update_layout_detail, update_layout_prijs
from db.datamanager import DataManager as dm
from models.ticket import Ticket

vertoningen_vandaag = dm.vertoningen_vandaag()
films = list({vertoning.film for vertoning in vertoningen_vandaag})
for film in films:
    film.load_api_data()

layout_films = create_layout_films(films)
layout_detail = create_layout_detail()

layout = [
    [
        sg.Column(layout_films, element_justification="center", key="-l_films-"),
        sg.Column(layout_detail, justification="center", element_justification="center",
                  key="-l_detail-", visible=False)
    ]
]

# Create the Window
window = sg.Window('Cinemax', layout, size=(
    1280, 720), element_justification="center")

# Event Loop to process "events" and get the "values" of the inputs
huidige_film = None
huidige_vertoning = None
tickets = []
while True:
    event, values = window.read() or (None, None)
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    if event.startswith("film-"):
        window["-l_films-"].update(visible=False)
        window["-l_detail-"].update(visible=True)
        huidige_film = next(
            film for film in films if film.id == int(event[5:]))
        vertoningen = [
            vertoning for vertoning in vertoningen_vandaag if vertoning.film == huidige_film]
        update_layout_detail(window, huidige_film, vertoningen)
    if event == "-terug_naar_films-":
        window["-l_films-"].update(visible=True)
        window["-l_detail-"].update(visible=False)
    if event == "-vertoningen-":
        if values["-vertoningen-"]:
            window["-naar_kopen-"].update(disabled=False)
            huidige_vertoning = values["-vertoningen-"][0]
        else:
            window["-naar_kopen-"].update(disabled=True)
    if event == "-naar_kopen-":
        window["-c_vertoningen-"].update(visible=False)
        window["-c_kopen-"].update(visible=True)
    if event == "-terug_naar_vertoningen-":
        window["-c_vertoningen-"].update(visible=True)
        window["-c_kopen-"].update(visible=False)
    if event in ["-volwassenen-", "-kinderen-"]:
        if huidige_vertoning:
            update_layout_prijs(window, huidige_vertoning)
    if event == "-koop_tickets-":
        if (huidige_vertoning):
            aantal_volwassenen = int(values["-volwassenen-"])
            aantal_kinderen = int(values["-kinderen-"])
            prijs_volwassene = Ticket.bereken_prijs(huidige_vertoning, False)
            prijs_kind = Ticket.bereken_prijs(huidige_vertoning, True)
            tickets = [Ticket(huidige_vertoning, True, prijs_kind) for _ in range(
                aantal_kinderen)] + [Ticket(huidige_vertoning, False, prijs_volwassene) for _ in range(aantal_volwassenen)]
            dm.insert_tickets(tickets)
            sg.Window("Tickets gekocht", [[sg.Text("Geniet van de film!", font="Helvetica 20")]], element_justification="center",
                      auto_close=True, auto_close_duration=3, margins=(50, 50), keep_on_top=True, no_titlebar=True).read(close=True)[0]
            window["-l_films-"].update(visible=True)
            window["-l_detail-"].update(visible=False)
            window["-c_vertoningen-"].update(visible=True)
            window["-c_kopen-"].update(visible=False)

window.close()
