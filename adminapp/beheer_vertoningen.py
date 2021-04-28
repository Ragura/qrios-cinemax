from ansimarkup import ansiprint as print
from utils.terminal import input_verplicht, maak_menu, input_getal, input_ja_nee, input_datum, input_tijd, clear_terminal
from db.datamanager import DataManager as dm
from prettytable import PrettyTable
from datetime import datetime
from zoneinfo import ZoneInfo


def beheer_vertoningen():
    clear_terminal()
    print("<white,blue>BEHEER VERTONINGEN</white,blue>")
    while True:
        menu_items = [
            "Vertoningen vandaag",
            "Vertoning toevoegen",
            "Vertoning verwijderen",
            ("Terug naar hoofdmenu", 0)
        ]
        maak_menu(menu_items)

        keuze = input_getal(
            "Kies een item uit het menu via het cijfer: ", col=range(len(menu_items)))

        if keuze == 0:
            break
        elif keuze == 1:
            vertoningen = sorted(dm.vertoningen_vandaag(),
                                 key=lambda x: (x.datum, x.zaal))
            tabel = PrettyTable()
            tabel.field_names = ["ID", "Film", "Moment", "Zaal", "3D"]
            for vertoning in vertoningen:
                tabel.add_row([vertoning.id, vertoning.film.titel, vertoning.moment, vertoning.zaal,
                               "Ja" if vertoning.drie_d else "Nee"])
            print(tabel)

        elif keuze == 2:
            vandaag = datetime.now(
                ZoneInfo("Europe/Brussels")).strftime('%d-%m-%Y')
            print(f"<bold>Datum: ({vandaag}) </bold>", end="")
            datum = input_datum(leeg_toegestaan=True)
            if not datum:
                datum = datetime.now(ZoneInfo("Europe/Brussels"))

            print(f"<bold>Titel film: </bold>", end="")
            search = input_verplicht()
            films = dm.zoek_films(titel=search)
            if not len(films):
                continue
            maak_menu([film.titel for film in films])
            index = input_getal(
                "Kies een film via het cijfer: ", col=range(1, len(films) + 1), leeg_toegestaan=True) or 1
            film = films[int(index) - 1]
            gegevens_vertoning = []
            while True:
                print(
                    f"<green>Aanmaken vertoningen voor {film.titel}, afbreken met lege invoer:</green>")
                print("<bold>Moment (UU:MM):</bold> ", end="")
                moment = input_tijd(leeg_toegestaan=True)
                if not moment:
                    break
                print("<bold>Zaal:</bold> ", end="")
                zaal = input_getal(leeg_toegestaan=True)
                if not zaal:
                    break
                print("<bold>3D? (J/N):</bold> ", end="")
                drie_d = input_ja_nee(leeg_toegestaan=True)
                if drie_d == None:
                    break
                gegevens_vertoning.append({
                    "uur": moment.hour,
                    "minuten": moment.minute,
                    "zaal": zaal,
                    "drie_d": drie_d
                })

            vertoningen = [{
                "film_id": film.id,
                "datum": datetime(
                    datum.year, datum.month, datum.day,
                    vertoning["uur"], vertoning["minuten"], tzinfo=ZoneInfo("Europe/Brussels")),
                "zaal": vertoning["zaal"],
                "drie_d": vertoning["drie_d"]
            } for vertoning in gegevens_vertoning]

            try:
                dm.add_vertoningen(vertoningen)
            except:
                print(
                    "<red><bold>Aanmaken vertoningen mislukt. Contacteer een administrator.</bold></red>")
            else:
                print("<green><bold>Vertoningen succesvol toegevoegd!</bold></green>")

        elif keuze == 3:
            search = input_getal(
                "Verwijder een vertoning op ID: ", leeg_toegestaan=True)
            if search:
                vertoning = dm.zoek_vertoning_by_id(int(search))
                if vertoning:
                    print(
                        f"<red>{str(vertoning)} voor film {vertoning.film.titel} zal verwijderd worden. Doorgaan? (Ja/Nee)</red>", end="")
                    if input_ja_nee():
                        dm.verwijder_vertoning(int(search))
                        print(
                            f"<green>Vertoning succesvol verwijderd.</green>")
            else:
                print("Geen vertoning met opgegeven ID gevonden.")

        print("\n<italic>Druk op een toets om verder te gaan...</italic>")
        input()
