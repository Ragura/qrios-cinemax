# Terminal application voor admin-kant

""" Moet kunnen:
    - Films toevoegen en verwijderen
    - Vertoningen toevoegen en verwijderen
    - Verkochte tickets opvragen + statistieken
"""

from ansimarkup import ansiprint as print
from utils.terminal import maak_menu, input_getal, clear_terminal
from adminapp.beheer_films import beheer_films
from adminapp.beheer_vertoningen import beheer_vertoningen
from adminapp.raadplegen_tickets import raadplegen_tickets

print("<black,yellow>CINEMAX ADMIN APP</black,yellow>")

while True:
    maak_menu([
        "Films beheren",
        "Vertoningen beheren",
        "Tickets raadplegen",
        ("Afsluiten", 0)
    ])

    keuze = input_getal(
        "Kies een item uit het menu via het cijfer: ", col=(0, 1, 2, 3))

    if keuze == 0:
        break
    elif keuze == 1:
        beheer_films()
    elif keuze == 2:
        beheer_vertoningen()
    elif keuze == 3:
        raadplegen_tickets()
    clear_terminal()
