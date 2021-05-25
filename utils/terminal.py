from typing import Union, Optional, Sequence
import os
from ansimarkup import ansiprint as print
from datetime import datetime
from zoneinfo import ZoneInfo


TNumeric = Union[int, float]


def maak_menu(items: list[Union[str, tuple[str, int]]], cijferkleur: str = "yellow") -> None:
    for index, item in enumerate(items):
        tekst = ""
        cijfer = 0
        if type(item) == str:
            tekst = item
            cijfer = index + 1
        elif type(item) == tuple and len(item) == 2:
            tekst, cijfer = item
        print(f"<{cijferkleur}>{cijfer}.</{cijferkleur}> {tekst}")


def input_verplicht(prompt: str = "") -> str:
    while True:
        text = input(prompt)
        if text:
            return text


def input_getal(prompt: str = "", minimum: Optional[TNumeric] = None, maximum: Optional[TNumeric] = None, col: Sequence[TNumeric] = [], leeg_toegestaan: bool = False) -> Optional[TNumeric]:
    """ Functie voor input van een geheel of decimaal getal

    Keyword arguments:
    minimum: Minimumwaarde voor getal
    maximum: Maximumwaarde voor getal
    col: Een reeks van geldige getallen
    leeg_toegestaan: Is een lege input toegestaan?
    """
    while True:
        number = input(prompt).strip()
        if not len(number) and leeg_toegestaan:
            return None
        try:
            number = int(number)
        except ValueError:
            try:
                number = float(number)
            except ValueError:
                print("Invoer is geen geldig getal.")
                continue
        if minimum and number < minimum:
            print("Ingevoerd getal is te klein.")
            continue
        if maximum and number > maximum:
            print("Ingevoerd getal is te groot.")
            continue
        if col and number not in col:
            print("Ingevoerd getal ligt buiten het geldige bereik.")
            continue
        break
    return number


def input_ja_nee(prompt: str = "", leeg_toegestaan: bool = False) -> Optional[bool]:
    while True:
        invoer = input(prompt)
        antwoorden_positief = ["j", "ja"]
        antwoorden_negatief = ["n", "nee", "neen"]
        if invoer == "" and leeg_toegestaan:
            return None
        if invoer.lower() in antwoorden_positief:
            return True
        if invoer.lower() in antwoorden_negatief:
            return False

        print("Geef een ja/nee antwoord.")


def input_datum(prompt: str = "", formaat: str = "%d-%m-%Y", leeg_toegestaan: bool = False) -> Optional[datetime]:
    while True:
        invoer = input(prompt)
        if invoer == "" and leeg_toegestaan:
            return None
        try:
            datum = datetime.strptime(invoer, formaat).replace(
                tzinfo=ZoneInfo("Europe/Brussels"))
            return datum
        except:
            print("Datum moet het volgende formaat hebben: DD-MM-JAAR")


def input_tijd(prompt: str = "", formaat: str = "%H:%M", leeg_toegestaan: bool = False) -> Optional[datetime]:
    while True:
        invoer = input(prompt)
        if invoer == "" and leeg_toegestaan:
            return None
        try:
            tijd = datetime.strptime(invoer, formaat)
            return tijd
        except:
            print("Tijd moet het volgende formaat hebben: UU:MM")


def clear_terminal() -> None:
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')


if __name__ == '__main__':
    pass
