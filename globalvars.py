# -*- coding: utf-8 -*-

"""

globalvars.py
Modulen innehåller globala variabler.

running - Så länge denna är True så är program igång.
size - storlek på pygame fönster.
whole_screenrect - storlek på pygamefönster som pygame.Rect-objekt.
curr_window - aktuell vy, antingen "game" eller "menu"

erasequeue - ta-bort-kö, koordinater som skickas hit färgläggs med svart färg.
blitqueue - blitqueue, koordinater och grafiknycklar som skickas hit visas på skärm.
graphics - innehåller ordlista med grafikobjekt, grafiknyckel används för att hämta objekt.
sounds - innehåller ordlista med ljudobjekt.

gameon - är True så länge orm lever.
switch_window - är True när man valt att växla mellan menyvy <-> spelvy

"""

import collections
import os
import pygame

if not pygame.font.get_init():
    pygame.font.init()

def init():
    """ Globala variabler (Används av fler program) """
    global size, curr_window, running, whole_screenrect
    running = True
    size = (800, 480)
    whole_screenrect = pygame.Rect((0, 0), size)
    curr_window = "menu"

    global black, white, yellow, green, brown
    black = (0, 0, 0)
    white = (255, 255, 255)
    yellow = (217, 219, 43)
    green = (45, 70, 34)
    brown = (127, 103, 54)

    global erasequeue, blitqueue, graphics, sounds
    erasequeue = []
    blitqueue = []
    graphics = {}
    sounds = {} 

    global font_medium, font_large, menufont_large, menufont_medium
    global menufont_small, mathfont # visar fråga och svarsalternativ
    font_medium = pygame.font.Font(None, 22)
    font_large = pygame.font.Font(None, 36)
    menufont_large = pygame.font.Font(os.path.join("font", "Serifa_Comica.ttf"), 24)
    menufont_medium = pygame.font.Font(os.path.join("font", "Serifa_Comica.ttf"), 18)
    menufont_small = pygame.font.Font(os.path.join("font", "Serifa_Comica.ttf"), 12)
    mathfont = pygame.font.Font(os.path.join("font", "ComicNeueSansID.ttf"), 18)

    global gameon, switch_window
    gameon = False   # Spel exekveras inte från start
    switch_window = True # Växla till menyvy vid start av program
