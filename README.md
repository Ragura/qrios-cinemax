# Cinemax Qrios

## Projectbeschrijving

Deze Python-applicatie voorziet een client en admin app voor het beheren en boeken van bioscoopvertoningen. Het is bedoeld als eindproject voor cursisten van de opleining TKO Programmeren bij CVO Qrios.

## Onderdelen

De admin app kan worden gestart via `admin.py` en is een terminal applicatie. De client app (kiosk-applicatie) kan worden gestart via `kiosk.py` en biedt een grafische interface gebouwd met [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/). Het bestand `cinemax.db` in de map `db` doet dienst als centrale *SQLite* databank.

## Installeren

Het project dient *gerunt* te worden binnen een *virtual environment*. Lees het volgende artikel om jezelf vertrouwd te maken met de stappen die je moet ondernemen om een *virtual environment* op poten te zetten: [https://www.studieanker.be/python/001-virtual_environments.html](https://www.studieanker.be/python/001-virtual_environments.html)

## Dependencies

Installeer de *dependencies* van het project binnen de *virtual environment* met:

```sh
pip install -r requirement.txt
```

## Config.ini en API Key

Je hoort een `config.ini` bestand aan te maken in de *root* van het project met de volgende structuur:

```ini
[DEFAULT]
# Jouw API_KEY voor toegang tot themoviedb.org
API_KEY = XXXXXXX
```

De applicatie maakt verbinding met de publieke API [The Movie Database](https://www.themoviedb.org), waaruit ze allerlei data voor films opvraagt. Om toegang te krijgen tot deze API moet je je registreren en een *API Key* aanvragen. Vervolgens plaats je de *key* die je gekregen hebt in het `config.ini` bestand.

## Databank maken en vullen

Het bestand `database.py` in de map `db` kan ook als applicatie worden uitgevoerd om de SQLite databank aan te maken en te vullen met tabellen en testgegevens voor films, vertoningen en tickets. De SQL-commando's die door de uitvoer van `database.py` uitgevoerd worden vind je in de bestanden `populate.sql` en `tables.sql` in de map `db`.
