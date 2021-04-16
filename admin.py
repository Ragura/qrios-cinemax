# Terminal application voor admin-kant

""" Moet kunnen:
    - Films toevoegen en verwijderen
    - Vertoningen toevoegen en verwijderen
    - Verkochte tickets opvragen + statistieken
"""

from ansimarkup import ansiprint as print
from utils.terminal import input_getal, clear_terminal
from adminapp.beheer_films import beheer_films
from adminapp.beheer_vertoningen import beheer_vertoningen
from adminapp.raadplegen_tickets import raadplegen_tickets

print("<black,yellow>CINEMAX ADMIN APP</black,yellow>")

while True:
    print("<yellow>1.</yellow> Films beheren")
    print("<yellow>2.</yellow> Vertoningen beheren")
    print("<yellow>3.</yellow> Tickets raadplegen")
    print("<yellow>0.</yellow> Afsluiten")

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
