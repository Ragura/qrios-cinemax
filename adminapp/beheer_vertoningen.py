from ansimarkup import ansiprint as print
from utils.terminal import input_verplicht, maak_menu, input_getal, input_ja_nee, input_datum, input_tijd, clear_terminal
from models.vertoning import Vertoning
from db.datamanager import DataManager as dm
from prettytable import PrettyTable
from datetime import datetime
from zoneinfo import ZoneInfo


def beheer_vertoningen():
    while True:
        clear_terminal()
        print("<white,blue>BEHEER VERTONINGEN</white,blue>")
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

                # Zaal kiezen
                zaal = None
                while not zaal:
                    print("<bold>Zaal:</bold> ", end="")
                    zaal_nummer = input_getal(leeg_toegestaan=True)
                    if not zaal_nummer:
                        break
                    zaal = dm.get_zaal_by_nummer(int(zaal_nummer))
                    if not zaal:
                        print(
                            f"<red>Zaal met nummer {zaal_nummer} bestaat niet.</red>")
                if not zaal:
                    break

                # Moment kiezen
                moment = None
                datum_moment = None
                while True:
                    print("<bold>Moment (UU:MM):</bold> ", end="")
                    moment = input_tijd(leeg_toegestaan=True)
                    if not moment:
                        break
                    datum_moment = datetime(
                        datum.year, datum.month, datum.day,
                        moment.hour, moment.minute, tzinfo=ZoneInfo("Europe/Brussels"))
                    # Nakijken of film wel past in het tijdslot
                    vertoning_overlap = dm.vertoning_overlap(
                        datum_moment, zaal.id, film.duur, 20)
                    if not vertoning_overlap:
                        moment = datum_moment
                        break
                    print(
                        f"<red>Vertoning valt samen met de vertoning van {vertoning_overlap.film.titel} om {vertoning_overlap.moment}.")

                if not moment:
                    break

                # 3D versie kiezen
                if zaal.drie_d_ondersteuning:
                    print("<bold>3D? (J/N):</bold> ", end="")
                    drie_d = input_ja_nee(leeg_toegestaan=True)
                    if drie_d == None:
                        break
                else:
                    drie_d = False

                vertoning = Vertoning(str(datum_moment), film, zaal, drie_d)

                try:
                    dm.add_vertoning(vertoning)
                except:
                    print(
                        "<red><bold>Aanmaken vertoningen mislukt. Contacteer een administrator.</bold></red>")
                else:
                    print(
                        "<green><bold>Vertoningen succesvol toegevoegd!</bold></green>")

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
