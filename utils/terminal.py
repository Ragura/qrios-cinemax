from typing import Union, Optional, Sequence
import os

TNumeric = Union[int, float]


def input_getal(prompt: str = "", minimum: Optional[TNumeric] = None, maximum: Optional[TNumeric] = None, col: Sequence[TNumeric] = []) -> TNumeric:
    """ Functie voor input van een geheel of decimaal getal

    Keyword arguments:
    minimum: Minimumwaarde voor getal
    maximum: Maximumwaarde voor getal
    col: Een reeks van geldige getallen
    """
    while True:
        number = input(prompt)
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


def clear_terminal():
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')


if __name__ == '__main__':
    pass
