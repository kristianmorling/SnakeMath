# -*- coding: utf-8 -*-

"""

###############
#SnakeMath 1.0#
###############

main.py, Linux 3.8.0-27-generic, Ubuntu 13.04, x86_64, Python 3.3.1
Kristian Mörling, krmo3719@student.su.se

Spelet är uppdelad i programfilerna main.py, screen.py, globalvars.py,
highscore.py och menu.py. screen.py anropas för att lägga till och ta
bort grafik på skärmen. globalvars.py samlar variabler som används i
flera programfiler. highscore.py läser in och sparar highscores. highscore.py
kontrollerar även ifall ett visst resultat är ett highscore. menu.py styr
hanterar programmets menyfönster.

I denna fil exekveras spelets "mainloop". Inför starten av programmet laddas
programmets resurser in. Skulle ett fel inträffa vid inladdning av dessa resurser
så avslutas programmet. I mainloopen anropas spelfönstret vid curr_window = "game".
Mainloopen anropar menyfönstret när curr_window = "menu". Dessa två fönster kommer
jag i programkommenterarna referera till som menyvy och spelvy.

Mer info: Mer utförlig beskrivning av programmets funktionalitet och vilka
referenser som har använts se Rapport.pdf bifogad i samma katalog som programmet.

Uppdatering 2013-09-09:
Programmet kunde inte starta på Windows eller MAC datorer. Detta berodde troligtvis på
att spelets bakgrundsmusik var av formatet FLAC. Bakgrundsmusiken har nu bytts ut mot
en WAV fil.

"""

import pygame
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

import os
import collections
from pygame.locals import *
import globalvars as gv
import game
import menu
import screen

# Skapa ordlista för spelvy och menyvy.
windows = {}

try:
    # Initiera globala variabler, skärm samt sätt fönstertitel.
    gv.init()
    window = pygame.display.set_mode(gv.size)
    pygame.display.set_caption("SnakeMath")
    
    # Aktivera endast Events som används.
    pygame.event.set_allowed(None) # blockera samtliga events
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.set_allowed(pygame.KEYDOWN)
    pygame.event.set_allowed(USEREVENT)

    # Skapa färgobjekt för att ta bort pixelytor med.
    gv.graphics["color_black"] = gv.black
    
    # Läs in ljudfiler.
    gv.sounds["theme"] = pygame.mixer.Sound(os.path.join("sound", "theme.wav"))
    gv.sounds["eat"] = pygame.mixer.Sound(os.path.join("sound", "eat.wav"))
    gv.sounds["highscore"]  = pygame.mixer.Sound(os.path.join("sound", "highscore.wav"))
    gv.sounds["wrong"]  = pygame.mixer.Sound(os.path.join("sound", "wrong.wav"))
    gv.sounds["correct"]  = pygame.mixer.Sound(os.path.join("sound", "correct.wav"))
    gv.sounds["select_menu"]  = pygame.mixer.Sound(os.path.join("sound", "menu_select.wav"))
    gv.sounds["back_menu"]  = pygame.mixer.Sound(os.path.join("sound", "menu_back.wav"))

    # Initiera resurser till Worldklass.
    text_line1 = "Press ENTER to restart game or"
    text_line2 = "ESC to return to the main menu."
    gv.graphics["introtext_line1"] = gv.menufont_large.render(text_line1, True, gv.yellow)
    gv.graphics["introtext_line2"] = gv.menufont_large.render(text_line2, True, gv.yellow)
    gv.graphics["food"] = pygame.image.load(os.path.join("pictures", "food.png")).convert_alpha()
    world = game.World()

    # Initiera resurser Snakeklass.
    gv.graphics["snake"] = pygame.image.load(os.path.join("pictures", "snake.png")).convert_alpha()
    snake = collections.deque() # skapa lista som representerar orm
    snake = game.Snake(snake, world)
    
    # Initiera resurser till GUIklass.
    gv.graphics["bg_gui"] = pygame.image.load(os.path.join("pictures", "gui.png")).convert()
    gv.graphics["happycursor_gui"] = pygame.image.load(os.path.join("pictures", "happycursor.png")).convert()
    gv.graphics["happybar_gui"] = pygame.image.load(os.path.join("pictures", "happybar.png")).convert()
    gui_rects = {
        "bg": pygame.Rect(600, 0, 200, 480),
        "happybar": pygame.Rect(628, 80, 155, 12),
        "happycursor": pygame.Rect(628, 80, 3, 12),
        "score": pygame.Rect(725, 25, 60, 25),
        "erase_qa": pygame.Rect(665, 105, 100, 150),
        "question": pygame.Rect(672, 110, 80, 50),
        "answer_alt1": pygame.Rect(680, 170, 70, 50),
        "answer_alt2": pygame.Rect(680, 200, 70, 50),
        "answer_alt3": pygame.Rect(680, 230, 70, 50)
        }
    gui = game.GUI(gui_rects)

    # Initiera resurser till Menuklass.
    highscore_header = "Player               Points" 
    gv.graphics["bg_main_menu"] = pygame.image.load(os.path.join("pictures", "mainmenu.png")).convert()
    gv.graphics["cursor_menu"] = pygame.image.load(os.path.join("pictures", "menucursor.png")).convert_alpha()
    gv.graphics["bg_help_menu"] = pygame.image.load(os.path.join("pictures", "helpmenu.png")).convert()
    gv.graphics["text_play_menu"] = gv.menufont_large.render("Play", True, gv.yellow)
    gv.graphics["text_table_menu"] = gv.menufont_large.render("Table", True, gv.yellow)
    gv.graphics["text_help_menu"] = gv.menufont_large.render("Help", True, gv.yellow)
    gv.graphics["text_exit_menu"] = gv.menufont_large.render("Exit", True, gv.yellow)
    gv.graphics["text_header_table"] = gv.menufont_large.render(highscore_header, True, gv.yellow)
    gv.graphics["text_underscore_table"] = gv.menufont_large.render("_ _ _ _", True, gv.yellow)
    gv.graphics["text_return_menu"] = gv.menufont_small.render("Press any key to return.", True, gv.yellow) 
    gv.graphics["text_help_meter"] = gv.menufont_small.render("Happymeter", True, gv.yellow)
    gv.graphics["text_help_arrowkeys"] = gv.menufont_small.render("Change  direction", True, gv.yellow)
    gv.graphics["text_help_nbrs"] = gv.menufont_small.render("Answer math problem", True, gv.yellow)
    gv.graphics["text_help_esc"] = gv.menufont_small.render("Return  to menu", True, gv.yellow)
    menu_rects = {
        "play":           pygame.Rect(380, 210, 230, 100),
        "table":          pygame.Rect(380, 240, 100, 100),
        "help":           pygame.Rect(380, 270, 100, 100),
        "exit":           pygame.Rect(380, 300, 100, 100),
        "cursor_on_PLAY": pygame.Rect(330, 220, 50, 50),
        "del_cursor":     pygame.Rect(295, 195, 70, 130),
        "del_text":       pygame.Rect(285, 180, 250, 200)
        }

    # Initiera resurser till Namedialogklass.
    gv.graphics["outer_dialog"] = pygame.Surface((320, 100))
    gv.graphics["inner_dialog"] = pygame.Surface((220, 40))
    pygame.draw.rect(gv.graphics["outer_dialog"], gv.brown, pygame.Rect(0,0,320,100), 5)
    pygame.draw.rect(gv.graphics["inner_dialog"], gv.brown, pygame.Rect(0,0,220,40), 3)
    gv.graphics["title_dialog"] = gv.menufont_medium.render("Highscore! Please type in your name.", True, gv.yellow)
    gv.graphics["cursor_dialog"] = gv.menufont_medium.render("_", True, (gv.yellow))
    erasename_rect = pygame.Rect(200, 216, 205, 30)
    namedialog = game.Namedialog(erasename_rect)

    # Skapa menyvy och spelvy.
    windows["menu"] = menu.Menu(menu_rects)
    windows["game"] = game.Game(world, gui, snake, namedialog)

except:
    print("Ett fel inträffade vid programinitiering! Avslutar spel.")
    import sys
    sys.exit(1)

# Starta klocka för ormrörelse.
pygame.time.set_timer(pygame.USEREVENT, 85)

# Måla all yta svart och starta musik.
window.fill(gv.graphics["color_black"])
pygame.display.flip()
gv.sounds["theme"].play(-1)

# Skapa indexvariabler för grafiklista.
GRAPHIC_KEY = 0
RECT = 1

while gv.running:

    # Vänta på knapptryck eller händelse för ormörelse.
    event = pygame.event.wait()

    # Ta hand om händelse.
    curr_window = gv.curr_window
    if event.type == QUIT:
        gv.running = False
    elif gv.switch_window:
        windows[curr_window].start() # växla mellan Spelvy <-> Menyvy
    elif event.type == KEYDOWN:
        windows[curr_window].inputhandler(event.key)
    elif event.type == USEREVENT:
        # Förflytta orm endast i spelvy och när orm inte är död.
        if gv.gameon and curr_window == "game":
            windows["game"].update()

    # Ta bort grafik.
    for rect in screen.get_erase():
        window.fill(gv.graphics["color_black"], rect) # ta bort pixelyta
        pygame.display.update(rect) 

    # Lägg till grafik.
    for obj in screen.get_blit():
        window.blit(gv.graphics[obj[GRAPHIC_KEY]], obj[RECT]) # lägg till pixelyta
        pygame.display.update(obj[RECT]) 

    # Töm grafiklistor.
    screen.truncate_erase()
    screen.truncate_blits()

pygame.quit()
