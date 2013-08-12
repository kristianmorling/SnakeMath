# -*- coding: utf-8 -*-

"""

screen.py

Modulen används för att fylla på/ta bort objekt ur
erasequeue och blitqueue.

Modulen anropas från modulerna main.py, game.py och menu.py.
main.py hämtar objekt och modulerna game.py och menu.py fyller
på grafikköerna med objekt.

Till ta-bort-kö:n läggs endast koordinat för yta att ta bort.
Till lägg-till-kö:n läggs både koordinat och grafiknyckel till.
Grafiknyckel används för indexering i globalvars.graphics ordlistan. 

"""

import globalvars as gv

def erase(rect):
    """ Ta bort objekt från ta-bort-kö """
    gv.erasequeue.append(rect)

def blit(key, rect):
    """ Lägg till objekt i lägg-till-kö """
    gv.blitqueue.append((key, rect))

def truncate_erase():
    """ Töm ta-bort-kö """
    gv.erasequeue = []

def truncate_blits():
    """ Töm lägg-till-kö """
    gv.blitqueue = []

def get_erase():
    """ Returnera ta-bort-kö """
    return gv.erasequeue

def get_blit():
    """ Returnera lägg-till-kö """
    return gv.blitqueue
