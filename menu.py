# -*- coding: utf-8 -*-

"""

menu.py
Modulen innehåller klassen Menu.
Klassen hanterar navigering i meny och visning av meny.

"""

import globalvars as gv
import highscore
import screen
import pygame
from pygame.locals import *

class Menu(object):
    
    """ Ett objekt som representerar en meny """
    
    PLAY = 0
    TABLE = 1
    HELP = 2
    EXIT = 3
    def  __init__(self, rects):
        """ Spara ordlista med rectobjekt och initiera variabler """
        self.rects = rects
        self.in_submenu = False # program startar i huvudmeny
        self.cursor_at = self.PLAY

    def inputhandler(self, key):
        """ Ta hand om inmatning """
        if self.in_submenu:
            # Vid knapptryck i submeny återgå till huvudmeny.
            self.show_main()
            self.in_submenu = False
        elif key == K_RETURN:
            # Öppna menyval.
            self.enter()
        elif key == K_UP:
            self.scroll(down = False)
        elif key == K_DOWN:
            self.scroll(down = True)

    def scroll(self, down):
        """ Ändra aktuellt menyval """
        if down:
            # Skrolla ner, om vid nedersta val gå till första val.
            self.cursor_at = (self.cursor_at + 1) % (self.EXIT + 1)
        else:
            # Skrolla upp, om vid första val gå till sista val.
            self.cursor_at = (self.cursor_at - 1) if self.cursor_at > self.PLAY else self.EXIT

        self.update_cursor()        

    def update_cursor(self):
        """ Flytta pekare till ny position """
        ROWGAP = 30 # vertikalt avstånd mellan menyval

        # Bestäm ny pekarpos genom att utgå från pekarpos för första menyval.
        cursorpos = pygame.Rect(self.rects["cursor_on_PLAY"])
        cursorpos.y = cursorpos.y + self.cursor_at * ROWGAP 

        # Dölj föregående pekare och visa ny pekare.
        screen.erase(self.rects["del_cursor"])
        screen.blit("cursor_menu", cursorpos)

    def enter(self):
        """ Gå in i eller går ur submeny """
        gv.sounds["select_menu"].play()
        
        if self.cursor_at == self.PLAY:
            self.show_game()
        elif self.cursor_at == self.TABLE:
            self.show_table()
        elif self.cursor_at == self.HELP:
            self.show_help()
        elif self.cursor_at == self.EXIT:
            gv.running = False

    def clearmenu(self):
        """ Tar bort text- och bildinnehåll i menyfönster """
        screen.erase(self.rects["del_text"])

    def show_game(self):
        """ Byter från menyvy till spelvy """
        gv.switch_window = True # visa spelvy
        gv.curr_window = "game"

    def show_table(self):
        """ Visar tabell/highscores """
        self.in_submenu = True

        # Töm aktuell meny för att sedan visa tabellmeny.
        self.clearmenu()
        screen.blit("text_header_table", pygame.Rect(295, 180, 100, 100))
        screen.blit("text_underscore_table", pygame.Rect(295, 185, 100, 100))
        screen.blit("text_underscore_table", pygame.Rect(445, 185, 100, 100))
        screen.blit("text_return_menu", pygame.Rect(340, 364, 150, 100))
        
        rownbr = 0
        FIRSTROW_Y = 210 # y-koordinat första rad
        NAME_X = 295 # x-koordinat för namn
        SCORE_X = 446 # x-koordinat för poäng
        ROWGAP = 15 # avstånd mellan poängrader
        SCORE = 0 # indexvariabel för highscorelista

        # Skriv ut samtliga rader.
        for h in highscore.get_highscores():
            y_coord = FIRSTROW_Y + rownbr * ROWGAP 
            col_name = "highscore_" + str((rownbr + 1)) + "_name" 
            col_score = "highscore_" + str((rownbr + 1)) + "_score" 
            gv.graphics[col_name] = gv.menufont_small.render((str(rownbr + 1) + ". " + h[1]), True, gv.yellow)
            gv.graphics[col_score] = gv.menufont_small.render(str(h[SCORE]), True, gv.yellow)
            screen.blit(col_name, pygame.Rect(NAME_X, y_coord, 100, 100))
            screen.blit(col_score, pygame.Rect(SCORE_X, y_coord, 100, 100))
            rownbr += 1

    def show_help(self):
        """ Visar hjälpmeny """
        self.in_submenu = True

        # Töm aktuell meny för att sedan visa hjälpmeny.
        self.clearmenu()
        screen.blit("bg_help_menu", pygame.Rect(295, 200, 500, 500))
        screen.blit("text_return_menu", pygame.Rect(340, 364, 150, 100))
        screen.blit("text_help_meter", pygame.Rect(395, 196, 200, 100))
        screen.blit("text_help_arrowkeys", pygame.Rect(395, 248, 200, 100))
        screen.blit("text_help_nbrs", pygame.Rect(395, 280, 200, 100))
        screen.blit("text_help_esc", pygame.Rect(395, 310, 200, 100))

    def show_main(self, goback_sound = True):
        """ Visar menyval i huvudmeny vid retur från submeny """
        self.cursor_at = self.PLAY

        # Spela ljud om föregående fönster var en submeny.
        if goback_sound:
            gv.sounds["back_menu"].play()

        # Töm aktuell meny för att sedan visa huvudmeny.
        self.clearmenu()
        screen.blit("text_play_menu", self.rects["play"])
        screen.blit("text_table_menu", self.rects["table"])
        screen.blit("text_help_menu", self.rects["help"])
        screen.blit("text_exit_menu", self.rects["exit"])
        screen.blit("cursor_menu", self.rects["cursor_on_PLAY"])

    def start(self):
        """ Visar menyvy """
        gv.switch_window = False

        # Ersätt hela fönstret med menyvy.
        screen.erase(gv.whole_screenrect)
        screen.blit("bg_main_menu", gv.whole_screenrect)
        self.show_main(goback_sound = False)        
