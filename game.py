# -*- coding: utf-8 -*-

"""

game.py
Modulen innehåller de klasser som används i programmets spelvy.
De klasser som ingår i modulen är World, GUI, Snake, Game och Namedialog.

World - Spelbana med lista över möjliga matställen. 
GUI - Spelvyns högra panel med belåtenhetsnivå, ställning, frågor och svarsalternativ.
Snake - Spelets orm.
Namedialog - Namndialog som används för att läsa in namn vid highscore.

Game klassen är den centrala klassen i modulen. Anrop till övriga klasser i
modulen sker med få undantag genom Game klassen.

"""

import highscore
import globalvars as gv
import math
import pygame
from pygame.locals import *
import random
import screen

WORLDRECT  = pygame.Rect(0, 0, 600, 480) # storlek på bana
STEP = 20 # bana är ett rutnät där varje ruta är 20x20 px

class World(object):
    """ Objekt för spelplan
    
    Objektet har koll på ytor på spelplanen som är tillgängliga att
    lägga ut mat på. Objektet ser även till att lägga ut äpplet på
    spelplanen samt sparar äpplets koordinat. Koordinaten sparas för
    att kunna kontrollera när ormens huvud kolliderar med äpplet.

    Objektet är superklass till Namedialog som anropar dess metoder
    add_to_world och erase_from_world.
    
    """
    
    def add_foodspot(self, foodspot):
        """ Lägg till foodspot som giltig matplats """
        self.foodspots.add((foodspot.x, foodspot.y))

    def remove_foodspot(self, foodspot):
        """ Ta bort foodspot från matplatser """
        try:
           self.foodspots.remove((foodspot.x,foodspot.y))
        except KeyError:
            # Kan genereras om matplats inte finns.
            pass 

    def reset_foodspots(self):
        """ Återställ lista över tillgängliga matplatser.

        Alla koordinater förutom ormens startposition blir matplatser.
        
        """
        
        global STEP
        self.foodspots = set()

        # Lägg till matplats så länge inte (240,210) <= (x, y) <= (300, 210).
        # STEP är storleken på varje ruta (STEPxSTEP) i spelplanens rutnät.
        # Då spelplanen är 600x480 är bredden 600/STEP och höjd 480/STEP.
        # Antal matplatser från start är (600/STEP * 480/STEP) - ormens
        # startlängd som är 3.
        [self.foodspots.add((x,y)) for x in range(0,600,STEP)
         for y in range(0,480,STEP) if not (x >= 240 and x <= 300 and y == 210)]

    def addfood(self):
        """ Lägg ut äpple på ett slumpmässigt matställe """
        global STEP
        X = 0
        
        # Välj ut ett slumpmässigt matställe.
        coordinate = random.sample(self.foodspots, 1)

        # Visa äpple på utvalt matställe.
        self.foodspot = pygame.Rect(coordinate[X], (STEP, STEP))
        screen.blit("food", self.foodspot)

    def foodhit(self, head):
        """ Kontrollera ifall huvud är på äpple """
        return self.foodspot.colliderect(head)

    def reset(self):
        """ Töm grafikinnehåll i värld """
        global WORLDRECT
        screen.erase(WORLDRECT)

    def introtext(self):
        """ Visa instruktioner för att starta spel/returnera till huvudmeny. """
        screen.blit("introtext_line1", pygame.Rect(115, 190, 400, 300))
        screen.blit("introtext_line2", pygame.Rect(115, 230, 400, 300))

    def add_to_world(self, obj, rect):
        """ Lägg till angivet objekt i värld (förlängs av Namedialog) """
        screen.blit(obj, rect)

    def remove_from_world(self, rect):
        """ Radera angiven yta från värld (förlängs av Namedialog) """
        screen.erase(rect)


class GUI(object):
    
    """ Beskriver panelen i spelvyn

        Panelen visar spelets antal poäng med frågor och svarsalternativ.
        Objektet innehåller metoder för att ändra fråga, poängställning
        och svarsalternativ.

        HAPPYLEVEL_STEP är värdet på antalet steg i x-led som varje ny
        belåtenhetsnivå motsvarar i panelen för ormens belåtenhetsnivå.

    """

    HAPPYLEVEL_STEP = 37
    
    def __init__(self, rects):
        """ Initialisera rect-objekt """
        self.rects = rects

    def add_question(self, operand1, operand2, operator, answer_options):
        """ Visa fråga med svarsalternativ i GUI """

        # Skapa grafik för fråga och svarsalternetiv.
        question = str(operand1) + " " + operator + " " + str(operand2)
        gv.graphics["question"] = gv.mathfont.render(question, True, gv.yellow)
        gv.graphics["answer_alt1"] = gv.mathfont.render\
                                     ("1. " + str(answer_options[0]),
                                      True, gv.yellow)
        gv.graphics["answer_alt2"] = gv.mathfont.render\
                                     ("2. " + str(answer_options[1]),
                                      True,
                                      gv.yellow)
        gv.graphics["answer_alt3"] = gv.mathfont.render\
                                     ("3. " + str(answer_options[2]),
                                      True,
                                      gv.yellow)

        # Visa fråga och svarsalternativ.
        self.erase_qa() # ta bort nuvarande fråga och svarsalternativ
        screen.blit("question", self.rects["question"])
        screen.blit("answer_alt1", self.rects["answer_alt1"])
        screen.blit("answer_alt2", self.rects["answer_alt2"])
        screen.blit("answer_alt3", self.rects["answer_alt3"])

    def erase_qa(self):
        """ Ta bort fråga och svarsalternativ från panel """
        screen.erase(self.rects["erase_qa"])

    def erase_score(self):
        """ Dölj text för antal poäng """
        screen.erase(self.rects["score"])    
        
    def update_happybar(self):
        """ Uppdatera pekare som visar ormens belåtenhetsnivå """

        # Ta bort aktuell belåtenhetsmätare och lägg till ny.
        screen.erase(self.rects["happybar"])
        screen.blit("happybar_gui", self.rects["happybar"])

        # Beräkna position för pekare och placera ut på mätare.
        # happycursor recten innehåller position för mätare.
        # Genom att använda x position för mätarens västra
        # sida så kan man räkna ut pekarens position på mätaren.
        rect = pygame.Rect(self.rects["happycursor"])
        rect.x = rect.x + self.HAPPYLEVEL_STEP * Snake.happylevel
        screen.blit("happycursor_gui", rect)

    def update_scorebar(self, score):
        """ Uppdatera poängruta med nytt poäng """

        # Skapa grafikobjekt för poängtext.
        gv.graphics["score"] = gv.menufont_large.render(str(score),
                                                        True,
                                                        gv.yellow)

        # Ta bort nuvarande poängtext och lägg till ny.
        screen.erase(self.rects["score"])
        screen.blit("score", self.rects["score"])

    def reset(self):
        """ Töm grafikinnehåll i GUI fönster. """
        screen.blit("bg_gui", self.rects["bg"])


class Snake(object):
    
    """ Beskriver spelets orm.

    Objektet innehåller metoder för att återställa orm vid omstart, förflytta
    orm, kontrollera om rörelse leder till kollision, ändra riktning och för
    att ändra ormens belåtenhetsnivå.

    Orm består av en länkad lista innehållande Rect-objekt. Vid rörelse
    försvinner ormens svans och ett nytt huvud läggs till framför det
    befintliga. När ormen äter ett äpple växer ormen med tre pluppar. Så för
    varje äpple ormen äter ökar grow-variabeln med tre. Om variabeln är större
    än noll så kommer ormen vid rörelse få ett nytt huvud men ormens svans
    kommer inte att raderas.

    NORTH, SOUTH, WEST och EAST är tuples för ormens rörelseriktning.
    Konstanterna används av objektets rörelsevektor och av movemetoden.
    Tuplen:s första element innehåller antal steg i x-led som väderstrecket
    motsvarar och det andra elementet antal steg i y-led.

    """

    # Rörelseriktningar.
    NORTH = (0, -1) 
    SOUTH = (0, 1)  
    WEST  = (-1, 0)
    EAST  = (1, 0)
    
    def __init__(self, snake, world):
        """ Initialisera objekt för orm och värld samt skapa rörelsevektor """
        self.snake = snake
        self.world = world

        self.move_vector = {
            (self.NORTH, K_RIGHT): self.EAST,
            (self.SOUTH, K_RIGHT): self.EAST,
            (self.NORTH, K_LEFT):  self.WEST,
            (self.SOUTH, K_LEFT):  self.WEST,
            (self.EAST,  K_UP):    self.NORTH,
            (self.WEST,  K_UP):    self.NORTH,
            (self.WEST,  K_DOWN):  self.SOUTH,
            (self.EAST,  K_DOWN):  self.SOUTH
            }

    def reset(self):
        """ Ställ in/återställ orm """
        global STEP
        Snake.happylevel = 2 # orm är lagomt belåten från start
        self.direction = self.EAST
        self.grow = 0
        self.turnlist = []

        # Bestäm ormens initialkoordinater.
        self.tail = pygame.Rect(8*STEP, 7*STEP, STEP, STEP)
        middle = pygame.Rect((9*STEP, 7*STEP), (STEP, STEP))
        self.head = pygame.Rect(10*STEP, 7*STEP, STEP, STEP)

        # Skapa orm med en längd på tre pluppar.
        self.snake.clear() # ta bort befintliga pluppar
        self.snake.append(self.tail)
        self.snake.append(middle)
        self.snake.append(self.head)

        # Visa orm i värld.
        for bodypart in self.snake:
            screen.blit("snake", bodypart)

    def move(self):
        """ Förflytta orm

        Returnera False vid krasch eller vid för låg belåtenhetsnivå.
        I annat fall returnera True. Värdet används i Gameklassen för
        att avgöra om spelet är över eller inte.

        """
        
        X = 0
        Y = 1
        global STEP
        global WORLDRECT

        # Ändra riktning på orm om svänglista inte är tom.
        if self.turnlist:
            self.direction = self.turnlist.pop(0)

        # Bestäm nytt huvud, huvud utanför värld hamnar på motsatt sida.
        head = pygame.Rect(self.head) # kopiera koordinater för nuvarande huvud
        head.x = (head.x + (self.direction[X] * STEP)) % WORLDRECT.width
        head.y = (head.y + (self.direction[Y] * STEP)) % WORLDRECT.height

        # Lägg till nytt huvud.
        self.head = head
        self.snake.append(head)

        # Ta bort nytt huvud från giltiga matställen och visa huvud.
        self.world.remove_foodspot(self.head)
        screen.erase(head)
        screen.blit("snake", head)

        # Ta bort svans för att simulera rörelse.
        if not self.grow:
            # Borttagen svans blir matplats.
            self.world.add_foodspot(self.tail)

            # Ta bort svans och bestäm ny svans.
            screen.erase(self.snake.popleft()) 
            self.tail = self.snake[0] # 1:a elementet = ny svans

        # Förläng orm genom att inte ta bort svans.
        else:
            self.grow -= 1

        return self.nocollision() and Snake.happylevel >= 0

    def nocollision(self):        
        """ Kontrollera efter kollision """
        collidepoints = list(self.snake) # kopiera orm
        collidepoints.pop() # ta bort huvud 
        return self.head.collidelist(collidepoints) == -1

    def turn(self, key):
        """ Byt riktning på orm om instruktion är giltig

        Riktning läggs till i svänglista som läses av objektets move
        metod vid rörelse.
        
        """

        LIST_EMPTY = 0
        LIST_FULL = 2
        try:
            length = len(self.turnlist)

            # Bestäm nästa riktning utifrån nuvarande riktning.
            if length == LIST_EMPTY:
                next_direction = self.move_vector[self.direction, key]
                self.turnlist.append(next_direction)

            # Bestäm riktning utifrån senast tillagda riktning i svänglista.
            # Lägg inte till riktning om lista är full.
            elif length < LIST_FULL:
                next_direction = self.move_vector\
                                 [self.turnlist[length - 1], key]
                self.turnlist.append(next_direction)
        except KeyError:
            # Genereras vid felaktigt kommando, t.ex. vid byt
            # riktning till NORR när nuvarande riktning är SÖDER.
            pass

    def happyup(self):
        """ Öka ormens belåtenshetsnivå om inte redan max. """
        if Snake.happylevel < 4:
            Snake.happylevel += 1

    def happydown(self):
        """ Minska ormens belåtenshetsnivå. """
        Snake.happylevel -= 1


class Game(object):
    
    """ Beskriver spelmotor som styr de grafiska spelklasserna

    Objektet innehåller metoder för att ta hand om inmatning,
    besvara frågor, uppdatera grafik i spelvy, skapa frågor,
    starta/avsluta spel samt återvända till menyvy.
    
    """
    
    def __init__(self, world, gui, snake, namedialog):
        """ Spara objekt och initialisera variabler """
        self.world = world
        self.gui = gui
        self.snake = snake
        self.namedialog = namedialog
        score = 0

    def inputhandler(self, key):
        """ Ta hand om inmatning """

        if Game.highscore:
            self.namedialog.inputhandler(key)
        elif key == K_ESCAPE:
            self.show_menu()
        elif gv.gameon:
            if key == K_1 or key == K_2 or key == K_3:
                if self.question_pending:
                    self.answer(key)
            elif key == K_UP or key == K_DOWN or key == K_RIGHT or \
                 key == K_LEFT:
                    self.snake.turn(key)
        elif key == K_RETURN:
                self.start()

    def show_menu(self):
        """ Återgå till menyvy """
        gv.switch_window = True # visa menyvy
        gv.curr_window = "menu"
        
    def answer(self, key):
        """ Kontrollera om svar är korrekt

        Denna metod anropas endast med key som teckenkoden
        för tangent 1, 2 eller 3.

        """

        # Subtrahera med värde för tangent 1 för att ge rätt index.
        # index 0 = tangent 1, index 1 = tangent 2, index 2 = tangent 3.
        index = key - K_1 

        # Lägg ut mat i värld om korrekt svar.
        if self.answer_alternatives[index] == self.result:
            gv.sounds["correct"].play()
            self.gui.erase_qa() # dölj fråga och svarsalternativ
            self.world.addfood() # lägg ut mat
            self.question_pending = False

        # Om fel svar, skapa ny fråga och minska belåtenhetsnivå.
        else: 
            gv.sounds["wrong"].play()
            self.generate_question()
            self.snake.happydown()
            
        self.gui.update_happybar()

    def update(self):
        """ Förflytta orm till ny position

        Vid krasch eller för låg belåtenhetsnivå avsluta spel
        och visa dialogfönster vid highscore.

        """

        # Orm har inte kraschat och är belåten.
        if self.snake.move():
            if not self.question_pending:
                if self.world.foodhit(self.snake.head):
                    gv.sounds["eat"].play()
                    self.snake.grow += 3
                    self.generate_question()
                    self.snake.happyup()
                    self.gui.update_happybar()
                    Game.score += 3
                    self.gui.update_scorebar(Game.score)

        # Game over.
        else:
            is_highscore = highscore.is_highscore(Game.score)
            self.stop()
            if is_highscore:
                Game.highscore = True
                gv.sounds["highscore"].play()
                self.namedialog.show_dialog()
            
    def generate_question(self):
        """ Skapa fråga och visa i GUI """
        minus_operator = random.randint(0, 1) 
        operand1 = random.randint(1, 99)
        operand2 = random.randint(1, 99)

        # Antag att operator är + och addera.
        operator = '+'
        self.result = operand1 + operand2

        # Skulle operator vara - så subtrahera.
        if minus_operator:
            operator = '-'
            self.result = int(math.fabs(operand1 - operand2))
            # Byt värden mellan operander om ena är större än andra.
            if operand2 > operand1:
                operand1, operand2 = operand2, operand1

        # Skapa svarsalternativ i lista och rör om ordningen.
        self.answer_alternatives = []
        alt1 = random.randint(self.result - 11, self.result - 1) 
        alt2 = random.randint(self.result + 1, self.result + 11)
        self.answer_alternatives.append(self.result)
        self.answer_alternatives.append(alt1)
        self.answer_alternatives.append(alt2)
        random.shuffle(self.answer_alternatives)
        self.question_pending = True
        
        # Visa fråga med svarsalternativ i GUI.
        self.gui.add_question(operand1, operand2, operator,
                              self.answer_alternatives)

    def start(self):
        """ Starta/Starta om spel samt återställ spelobjekt """
        gv.switch_window = False # är True när spel startas från menyvy 
        self.world.reset()
        self.gui.reset()
        Game.score = 0
        Game.highscore = False
        self.gui.update_scorebar(self.score)
        self.snake.reset()
        self.world.reset_foodspots()
        self.gui.update_happybar()
        self.generate_question()
        gv.gameon = True
        
    def stop(self):
        """ Avsluta spel samt återställ spelbojekt """
        gv.gameon = False
        
        # Töm listor över grafiska objekt att lägga till och ta bort.
        # Grafiska speluppdateringar är inte nödvändiga när spel är över.
        screen.truncate_erase()
        screen.truncate_blits()
        
        self.world.reset()
        self.gui.reset()
        self.world.introtext()
        

class Namedialog(World):
    
    """ Beskriver dialogfönster för inmatning av namn.

    Objektet innehåller metoder för att visa/dölja dialogfönstret,
    visa instruktionstext för att starta om spel eller återvända till
    meny och metoder för att ta hand om inmatning.

    Metoderna för att visa dialogfönster och dölja dialogfönster
    "förlänger" (extends) superklassens metoder add_to_world och
    remove_from_world.

    """
    
    def __init__(self, erasename_rect):
        """ Initialisera borttagningsrect och teckenlista för namn """
        self.erasename_rect = erasename_rect
        self.name = [] # teckenlista som utgör namn

    def inputhandler(self, key):
        """ Ta hand om inmatning """
        MAXCHARS = 13 # namn är högst 13 tecken
        refresh = True

        # Lägg till tecken om ASCII och om antal tecken < max.
        if self._isascii(key):
            if len(self.name) < MAXCHARS:
                self.name.append(chr(key))
        # Ta bort tecken.
        elif key == K_BACKSPACE:
            if self.name:
                self.name.pop()
        # Spara highscore om namnfält ej tomt och RETURN-tangent.
        elif key == K_RETURN:
            if self.name:
                refresh = False
                highscore.add_highscore(Game.score, ''.join(self.name))
                Game.highscore = False
                self.hide_dialog()

        # Visa eventuella borttagna/tillagda tecken. 
        if refresh:
            self._refresh_dialog()

    def _isascii(self, char):
        """ Kontrollera om tecken är ASCII """
        return char >= K_a and char <= K_z

    def _refresh_dialog(self):
        """ Uppdatera namn i namnfält

        Anropas när tecken lagts till eller tagits bort.
        
        """
        
        nbr_of_chars = len(self.name)

        # Dölj nuvarande namn och skapa nytt grafikobjekt för namn.
        super().remove_from_world(self.erasename_rect)
        gv.graphics["playername"] = gv.menufont_medium.render\
                                    (''.join(self.name), True, gv.yellow)

        # Bestäm centerposition och visa nyskapat namnobjekt.
        NAME_X = 297
        NAME_Y = 220
        namerect = gv.graphics["playername"].get_rect()
        namerect.x = NAME_X - (namerect.width / 2)
        namerect.y = NAME_Y
        screen.blit("playername", namerect)

        # Bestäm position för textpekare och visa textpekare.
        CURSOR_X = namerect.x + namerect.width + 2 # precis intill namn
        screen.blit("cursor_dialog", pygame.Rect(CURSOR_X, 220, 30, 30))

    def hide_dialog(self):
        """ Göm dialogfönster, ta bort namn och visar introtext. """
        super().reset()
        super().introtext()
        self.name = [] # ta bort namn inför nästa inmatning

    def show_dialog(self):
        """ Visa dialogfönster utan inmatat namn. """
        super().add_to_world("outer_dialog", pygame.Rect(140, 170, 320, 100))
        super().add_to_world("inner_dialog", pygame.Rect(190, 210, 220, 40))
        super().add_to_world("title_dialog", pygame.Rect(148, 180, 302, 40))
        super().add_to_world("cursor_dialog", pygame.Rect(299, 220, 30, 30))

