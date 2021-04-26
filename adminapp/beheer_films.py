from configparser import ConfigParser
from ansimarkup import ansiprint as print
from utils.terminal import maak_menu, input_getal, input_ja_nee, clear_terminal
from db.datamanager import DataManager as dm
from prettytable import PrettyTable
import requests


def beheer_films():
    clear_terminal()
    config = ConfigParser()
    config.read("config.ini")
    print("<white,blue>BEHEER FILMS</white,blue>")
    while True:
        menu_items = [
            "Lijst films",
            "Film toevoegen",
            "Film zoeken",
            "Film verwijderen",
            ("Terug naar hoofdmenu", 0)
        ]
        maak_menu(menu_items)

        keuze = input_getal(
            "Kies een item uit het menu via het cijfer: ", col=range(len(menu_items)))

        if keuze == 0:
            break
        elif keuze == 1:
            films = sorted(dm.alle_films(), key=lambda x: x.titel)
            tabel = PrettyTable()
            tabel.field_names = ["ID", "Titel", "Duur", "KNT", "IMDB_ID"]
            for film in films:
                tabel.add_row([film.id, film.titel, film.duur,
                               "Ja" if film.knt else "Nee", film.imdb_id])
            print(tabel)

        elif keuze == 2:
            while True:
                print("<bold>IMDB ID van film: </bold>", end="")
                imdb_id = input()
                if imdb_id.startswith("tt") and len(imdb_id) == 9:
                    break
                print("Ongeldig IMDB ID")

            parameters = {
                "api_key": config["DEFAULT"]["API_KEY"],
                "external_source": "imdb_id",
                "language": "nl-NL"
            }
            try:
                data = requests.get(
                    f"https://api.themoviedb.org/3/find/{imdb_id}", params=parameters).json()
            except:
                print("Fout bij ophalen filminformatie via API.")
                break

            if not data.get("movie_results"):
                print("Film niet gevonden.")
                break

            film_data = data.get("movie_results")[0]
            film_data = requests.get(
                f"https://api.themoviedb.org/3/movie/{film_data['id']}", parameters).json()

            print(f"<bold>Titel: ({film_data['title']}) </bold>", end="")
            titel = input()
            if not titel:
                titel = film_data["title"]

            print(f"<bold>Duur: ({film_data['runtime']}) </bold>", end="")
            duur = input_getal(leeg_toegestaan=True)
            if not duur:
                duur = film_data["runtime"]

            print(
                f"<bold>KNT: ({'Ja' if film_data['adult'] else 'Nee'}) </bold>", end="")
            knt = input_ja_nee(leeg_toegestaan=True)
            if not knt:
                knt = film_data["adult"]

            try:
                dm.add_film(titel, int(duur), imdb_id, knt)
            except:
                print(
                    "<red><bold>Aanmaken film mislukt. Contacteer een administrator.</bold></red>")
            else:
                print("<green><bold>Film succesvol toegevoegd!</bold></green>")

        elif keuze == 3:
            search = input("Zoek een film op titel of IMDB ID: ")
            if search:
                resultaten = dm.zoek_films(titel=search, imdb_id=search)
                resultaten.sort(key=lambda f: f.titel)
                tabel = PrettyTable()
                tabel.field_names = ["ID", "Titel", "Duur", "KNT", "IMDB_ID"]
                for film in resultaten:
                    tabel.add_row([film.id, film.titel, film.duur,
                                   "Ja" if film.knt else "Nee", film.imdb_id])
                print(tabel)

        elif keuze == 4:
            search = input_getal(
                "Verwijder een film op ID: ", leeg_toegestaan=True)
            if search:
                films = dm.zoek_films(id=int(search))
                if films:
                    aantal_vertoningen = dm.tel_vertoningen(
                        film_id=int(search))
                    if aantal_vertoningen:
                        print(
                            f"<red>OPGELET: Er zijn {aantal_vertoningen} vertoningen voor <b>{films[0].titel}</b> die ook zullen worden verwijderd. Doorgaan? (Ja/Nee)</red>", end="")
                        if input_ja_nee():
                            dm.verwijder_film(int(search))
                            print(
                                f"<green><b>{films[0].titel}</b> succesvol verwijderd.</green>")
                    else:
                        dm.verwijder_film(int(search))
                        print(
                            f"<green><b>{films[0].titel}</b> succesvol verwijderd.</green>")
                else:
                    print("Geen film met opgegeven ID gevonden.")

        print("\n<italic>Druk op een toets om verder te gaan...</italic>")
        input()
