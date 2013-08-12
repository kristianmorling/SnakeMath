import os

"""

highscore.py
Modulen används för att läsa in och skriva highscore. Modulen består även
av en funktion som anropas för att kontrollera ifall det angivna argumentet
är ett highscore.

Modulen består av funktionerna _load_highscores, add_highscore, _save_highscore,
is_highscore, _sort och get_highscores. Modulens globala variabel highscores
innehåller inlästa highscores efter anrop av _load_highscores som anropas
automatiskt vid import av modul. För att inläsningen av highscore.txt filen ska
lyckas, så måste varje highscore vara skriven på en enskild rad enligt syntaxen
RESULTAT NAMN, där RESULTAT är ett heltal och NAMN en sträng.

Den globala variabeln MAXSCORES innehåller max antal rader
en lista med highscores kan bestå utav.

"""

highscores = []
MAXSCORES = 10

# Indexvariabler för highscores.
SCORE = 0
NAME = 1

def _load_highscores():
    """ Laddar in fil med highscore """
    global highscores, MAXSCORES
    global NAME, SCORE
    
    try:
        score_nbr = 0 # aktuell rad i fil
        with open(os.path.join("data", "highscore.txt"), "r") as f:
            for line in f.readlines():
                if score_nbr == MAXSCORES: # läs inte fler rader än maxantal
                    break

                # Om inte blank rad, spara rad.
                if not line.isspace():
                    line = line.replace("\n", " ") # ta bort radslutstecken
                    line = line.split()
                    try:
                        highscores.append((int(line[SCORE]), line[NAME]))
                        score_nbr += 1
                    except IndexError as e:
                        print("Öppna highscorefil - ", end="")
                        print("Fel vid inläsning av rad från highscore.txt!")
                        print(e)
        _sort()
    except IOError:
        print("Läs in highscorefil - Kunde inte öppna highscore.txt!")

def _sort():
    """ Sortera med högsta poäng först """
    global highscores
    highscores.sort(reverse = True)

def add_highscore(score, player):
    """ Lägger till highscore och uppdaterar fil """
    global highscores, MAXSCORES

    # Lägg till highscore.
    highscores.append((score, player))
    _sort()

    # Om fler än MAXSCORES rader, ta bort en rad.
    if len(highscores) > MAXSCORES:
        highscores.pop()
    
    _save_highscores()

def _save_highscores():
    """ Sparar highscores lista till highscore.txt """
    global highscores
    global NAME, SCORE
    
    try:
        with open(os.path.join("data", "highscore.txt"), "w") as f:
            for line in highscores:
                f.write(str(line[SCORE]) + " " + line[NAME] + "\n")
    except IOError as e:
        print("Spara highscorefil - ", end="")
        print("Kunde inte öppna highscore.txt!")
        print(e)

def is_highscore(score):
    """ Returnera True om lista är tom eller score >= lägsta poäng """
    global highscores, MAXSCORES, SCORE

    try:
        # Tolka som highscore om lista inte är full.
        if len(highscores) < MAXSCORES:
            return True
        
        # Tolka som highscore om större än sistplacerade.
        LAST_PLACE = len(highscores) - 1
        if  score > highscores[LAST_PLACE][SCORE]:
            return True
    except IndexError as e:
        print("Kontroll av highscore.")
        print(e)
    
    return False

def get_highscores():
    """ Returnera lista med highscores """
    global highscores
    return highscores

_load_highscores() # laddas automatiskt import
