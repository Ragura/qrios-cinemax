from ansimarkup import ansiprint as print
from utils.terminal import input_verplicht, maak_menu, input_getal, input_ja_nee, input_datum, input_tijd, clear_terminal
from db.datamanager import DataManager as dm
from prettytable import PrettyTable
from datetime import datetime
from zoneinfo import ZoneInfo


def raadplegen_tickets():
    while True:
        clear_terminal()
        print("<white,blue>BEHEER VERTONINGEN</white,blue>")
        menu_items = [
            "Wekelijkse ticketverkoop",
            "Rangschikking filmopbrengst",
            ("Terug naar hoofdmenu", 0)
        ]
        maak_menu(menu_items)

        keuze = input_getal(
            "Kies een item uit het menu via het cijfer: ", col=range(len(menu_items)))

        if keuze == 0:
            break
        elif keuze == 1:
            vandaag = datetime.now(ZoneInfo("Europe/Brussels"))
            huidig_jaar = vandaag.year
            tickets = dm.tickets_periode(
                str(datetime(huidig_jaar, 1, 1, tzinfo=ZoneInfo("Europe/Brussels"))))

            week_tickets = [
                [
                    ticket for ticket in tickets
                    if datetime.fromisoformat(ticket.datum_verkoop).isocalendar()[1] == week
                ] for week in range(1, 53)
            ]

            for idx, week in enumerate(week_tickets):
                if not week:
                    continue
                print(f"Week {idx + 1}:")
                tickets_per_film = {}
                for ticket in week:
                    tickets_per_film[ticket.vertoning.film.titel] = (
                        tickets_per_film.get(ticket.vertoning.film.titel) or 0) + 1

                tabel = PrettyTable(["Film", "Verkochte Tickets"])
                tabel.add_rows([(film, aantal)
                               for film, aantal in tickets_per_film.items()])
                print(tabel)
        elif keuze == 2:
            omzet_per_film = dm.tickets_omzet()
            tabel = PrettyTable(["Film", "Omzet"])
            tabel.add_rows(omzet_per_film)
            print(tabel)

        print("\n<italic>Druk op een toets om verder te gaan...</italic>")
        input()
