import PySimpleGUI as sg
from models.film import Film
from models.vertoning import Vertoning
from models.ticket import Ticket
from layouts.gui_utils import get_img_data


def create_layout_detail():

    poster = sg.Image(data="", key="-poster-")

    layout = [
        [
            sg.Column([[poster]]),
            sg.Column([
                [sg.Text("", size=(50, 1), font="Helvetica 24",
                         key="-titel-")],
                [
                    sg.Text("", size=(8, 1), font="Helvetica 14",
                            key="-duur-")
                ],
                [sg.Text("KINDEREN NIET TOEGELATEN", font="Helvetica 14", text_color="red",
                         key="-knt-", visible=False)],
                [sg.Text("", size=(50, 10), font="Helvetica 18",
                         key="-beschrijving-")],

                [
                    sg.Column([
                        [sg.Listbox([], size=(50, 5), font="Helvetica 18", enable_events=True,
                                    key="-vertoningen-")],
                        [sg.Button("Terug naar films", font="Helvetica 16", key="-terug_naar_films-"), sg.Button(
                            "Vertoning kiezen", disabled=True, font="Helvetica 16", pad=(300, 0), key="-naar_kopen-")]
                    ], key="-c_vertoningen-"),

                    sg.Column([
                        [
                            sg.Text("Aantal volwassenen: ",
                                    font="Helvetica 18"),
                            sg.Spin(values=[i for i in range(
                                999)], font="Helvetica 18", enable_events=True, key="-volwassenen-"),
                            sg.Text("Aantal kinderen: ", font="Helvetica 18",
                                    visible=True, key="-label_kinderen-"),
                            sg.Spin(values=[i for i in range(
                                999)], font="Helvetica 18", enable_events=True, key="-kinderen-", visible=True)
                        ],
                        [
                            sg.Text("Prijs: €", font="Helvetica 18"),
                            sg.Text("0.00", font="Helvetica 18", key="-prijs-")
                        ],
                        [sg.Button("Andere vertoning", font="Helvetica 16", key="-terug_naar_vertoningen-"), sg.Button(
                            "Tickets kopen", disabled=True, font="Helvetica 16", pad=(300, 0), key="-koop_tickets-")]
                    ], key="-c_kopen-", visible=False),
                ]
            ])
        ]
    ]

    return layout


def update_layout_detail(window: sg.Window, film: Film, vertoningen: list[Vertoning]):
    # Update poster
    window["-poster-"].update(data=get_img_data(film.get_afbeelding(),
                              maxsize=(500, 500), first=True))
    # Update titel
    window["-titel-"].update(value=film.titel)
    # Update duur
    uren = int(film.duur / 60)
    minuten = film.duur % 60
    window["-duur-"].update(value=f"{uren}u {minuten}min")
    # Update KNT
    window["-knt-"].update(visible=bool(film.knt))
    window["-label_kinderen-"].update(visible=not bool(film.knt))
    window["-kinderen-"].update(visible=not bool(film.knt))
    # Update beschrijving
    window["-beschrijving-"].update(value=film.beschrijving)
    # Update vertoningen
    window["-vertoningen-"].update(values=vertoningen)
    # Reset disabled "Vertoning Kiezen" knop
    window["-naar_kopen-"].update(disabled=True)
    # Reset aantal volwassenen en kinderen
    window["-volwassenen-"].update(value=0)
    window["-kinderen-"].update(value=0)


def update_layout_prijs(window: sg.Window, vertoning: Vertoning):
    totaal_prijs = Ticket.bereken_prijs(vertoning, False) * int(window["-volwassenen-"].get()) \
        + Ticket.bereken_prijs(vertoning, True) * \
        int(window["-kinderen-"].get())

    window["-prijs-"].update(value=str(totaal_prijs))
    if totaal_prijs > 0:
        window["-koop_tickets-"].update(disabled=False)
    else:
        window["-koop_tickets-"].update(disabled=True)
