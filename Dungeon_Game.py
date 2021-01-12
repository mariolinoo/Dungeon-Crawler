from roll import wurfel
import random
import PySimpleGUI as sg
import sys
import dungeon_creater_01
import os
import glob 

#2D Dungeoncrawler
#Class für Hero
"""Importiert oder erstellt eine neue Map und sucht passende Spawnstellen für die Monster und den Hero"""


def populate_dungeon( verbose = False):
    width = len(Game.current_level[0])
    hight = len(Game.current_level)
    tiles = [spot for sublist in Game.current_level for spot in sublist]
    empty_tiles = tiles.count(".")
    monster_anzahl = (empty_tiles//10) or 1 # or ist für den Fall, dass es eine Null rauskommt
    #Platziert monster_anzahl Monster im Dungeon
    for i in range(monster_anzahl+1):
        setzen = False
        if verbose:
            print(f" Sucht nach einem Sitzplatz für Affe{i}")
        while not setzen:
            for j, spot in enumerate(tiles):
                if spot == ".":
                    frei = True
                    if i == 0:
                        if random.random()<0.005:
                            Hero(j%width, j//width)
                            setzen = True
                            break
                    else:
                        for mi in Game.zoo:
                            if mi.x == j%width and mi.y == j//width:
                                frei = False
                                break
                        if frei:
                            if random.random()<0.005:
                                Monkey(j%width, j//width)
                                if verbose:
                                    print(f"Monkey{i} hingesetzt")
                                setzen = True
                                break
    if verbose:
        print("Alle Affen sitzten")
        
                               
def bewegung():
    """returns dx und dy"""
    return random.randint(-1,1), random.randint(-1,1)

def strike(attacker, defender):
    to_hit, to_hit_string = wurfel(attacker.to_hit_dice)
    to_defend, to_defend_string = wurfel(defender.to_defense_dice)
    dmg, dmg_string = wurfel(attacker.dmg_dice)
    prot, prot_string = wurfel(defender.protection_dice)
    print(f"{attacker.__class__.__name__} swings with {to_hit_string} at {defender.__class__.__name__} with defense chance {to_defend_string}")  
    if to_defend >= to_hit:
        print("Attack failed")
        return
    print(f"{attacker.__class__.__name__} hits with {dmg_string} {defender.__class__.__name__} with {prot_string} armor")
    if dmg<=prot:
        print("No damage")
        return
    dmg-=prot
    defender.hp-=dmg
    print(f"{defender.__class__.__name__} looses {dmg}hp and has {defender.hp}hp left")
    
    
def fight(attacker, defender):
    strike(attacker, defender)
    if defender.hp <= 0:
        print(f"{defender.__class__.__name__} is dead")
        return
    print("Counterstrike")
    strike(defender, attacker)
    if attacker.hp <= 0:
        print(f"{attacker.__class__.__name__} is dead")           
        
def alive():
    """clean dead monsters and change the dungeon if necessary"""
    for mi in Game.zoo:
        if mi.hp <= 0:
            Game.graveyard.append(mi)
            Game.current_level[mi.y][mi.x] = "X" if mi.__class__.__name__ == "Hero" else "x"
    #listcomprehension
    Game.zoo = [mi for mi in Game.zoo if mi.hp > 0]


def print_dungeon():
    # Dungeon zeichnen
    # enumerate nummeriert Inhalte, erzeugt eine Variable dafür
    dungeon_string=""
    for y, line in enumerate(Game.current_level):
        # print(y,line) Ausgabe
        for x, char in enumerate(line):
            # char ist nicht reserviert durch python (zusatzmodule können char vlt reservieren)
            for mi in Game.zoo:
                if x == mi.x and y == mi.y:
                    #print(mi.logo, end='')
                    dungeon_string += mi.logo
                    break
            else:
                #print(char, end='')
                dungeon_string += char
        #print()
        dungeon_string += "\n"
    return dungeon_string

class Game:
    """Container für globale Variablen"""
    zoo = []  # Monsterliste
    graveyard = []
    current_level = []

class Monster:
    """Generic Monsterclass"""
    #Classatribute
    number=0 #Monsterid

    def __init__(self, x=1, y=1, hp=10, logo='M'): #self ist durch constructor definiert und kann beliebig gewählt werden
        self.number=Monster.number
        Monster.number+=1
        Game.zoo.append(self)
        self.hp=hp
        self.x=x
        self.y=y
        self.logo=logo
        self.to_hit_dice="1d2"
        self.dmg_dice="1D5"
        self.to_defense_dice="1D2"
        self.protection_dice="1d2"
    
    def monstercrash(self, x, y):
        for mi in Game.zoo:
            if mi.x==x and mi.y==y and mi.number!=self.number: #für Hero soll eine attackbefehl im nächsten schritt prog werden
                return mi
        return None
        
    def attack(self, target):
        if target.__class__.__name__ == "Hero":
            print("Attacking Hero")
            fight(self, target)
                       
        else:
            print("avoiding friend")
            
        
        
    def ai(self, verbose = False):
        dx,dy=bewegung()
        target = self.monstercrash(self.x+dx , self.y+dy)
        if target != None :
            self.attack(target)
            return
        target = Game.current_level[self.y+dy][self.x+dx]
        if target == '#' :
            if verbose:
                print(f"{self.__class__.__name__} #{self.number} hits a wall")            
        elif target == ".":
            self.x+=dx
            self.y+=dy
        else:
            print(f"{self.__class__.__name__} #{self.number} looks through the fence")
        return

class Monkey(Monster):
    def __init__(self,  x=1, y=1, hp=10, logo='@'):
        super().__init__(x,y,hp,logo) # ruft die eltern funktion auf
        self.to_hit_dice="1d3"
        self.dmg_dice="1D5"
        self.to_defense_dice="1D3"
        self.protection_dice="1d3"
    
    def ai(self, verbose = False):
        super().ai()
        

class Hero(Monster):
    """Hero ist ein Kind von Monster"""
    def __init__(self,  x=1, y=1, hp=15, logo='H'):
        super().__init__(x,y,hp,logo) # ruft die eltern funktion auf
        self.to_hit_dice="1D5"
        self.dmg_dice="1D6"
        self.to_defense_dice="1D4"
        self.protection_dice="1d3"
        self.bag = [Pickaxe()]
        
    def attack(self, target):
        if target.__class__.__name__ != "Hero":
            print("attacking monster")
            fight(self, target)
        else:
            print("avoiding friend")
    
    def ai(selfl):
        return 0,0

    def has_item(self, item_name):
        for item in self.bag:
            if item.__class__.__name__ == item_name:
                return True
        return False

    def dig(self, target, dx, dy):
        if target == "#":
            Game.current_level[self.y+dy][self.x+dx] = "."


    def bewegung(self, command = ""):
        #command=input("wasd? Enter:")
        dx,dy=0,0
        if command == 'left':
            dx=-1
        elif command == 'down':
            dy=1
        elif command == 'right':
            dx=1
        elif command == 'up':
            dy=-1    
        elif command == 'wait':
            pass
        #Test for attack
        target=self.monstercrash(self.x+dx, self.y+dy)
        if target != None:
            self.attack(target)
            dx,dy=0,0
            return
        #Test for Moving 
        target = Game.current_level[self.y+dy][self.x+dx]
        if target == '#':
            if self.has_item("Pickaxe"):
                self.dig(target, dx, dy)
            else:
                print("Hero avoided Wall")

        elif target == '.':
            self.x+=dx
            self.y+=dy

        else:
            print("Impossible move")

class Item:
    pass #ist eine leere Funktion

class Pickaxe(Item):
    pass



def init(dungeon_name = None, verbose = False):
    #Dungeon wird gesucht und notfalls selber erstellt
    if dungeon_name is None:
        while True:
            dungeon_list = glob.glob("*.dungeon")
            if len(dungeon_list) > 0:
                dungeon_name = dungeon_list[0]
                break           
            else:
                dungeon_creater_01.main(autosave = True)

    #Lädt Dungeon rein
    with open(dungeon_name) as dungeon:
        Game.current_level = dungeon.readlines()

    #Zerlegt den Dungeon in Zeilen und setzt die Monster und den Hero
    Game.current_level=[list(row)[:-1] for row in Game.current_level]
    if verbose:
        print("Level loaded")
    populate_dungeon()
    hero = Game.zoo[0]

    return hero


def main(dungeon_name = None, verbose = False):
    # Define the window's contents
    game_round = 1
    hero = init(dungeon_name, verbose)
    dungeon_string = print_dungeon()

    layout =    [
                [sg.Text(dungeon_string, size=(60,20), key = "dungeon", font = ("Mono", 18), text_color="black")],
                [sg.Output(size=(60, 10), pad=(40,20,0,0), key="output", font = ("Mono", 12))],
                [sg.Text("", size=(7,1)),sg.Button('\u2191', size=(5,1), key = "up"), sg.Text("", size=(5,1))],
                [sg.Button("\u2190", size=(5,1),key = "left"), sg.Button("W8", size = (5,1), key = "wait"),  sg.Button("\u2192", size=(5,1), key = "right")],
                [sg.Text("", size=(7,1)), sg.Button("\u2193", size=(5,1), key = "down"), sg.Text("", size=(5,1))],
                [sg.Text("What is your command?"), sg.Input(key='command')],
                [sg.Button('Ok'), sg.Button('Quit')],
                ]

    # Create the window
    window = sg.Window('Dungeon Crawler', layout)

    # Display and interact with the Window using an Event Loop
    window.finalize()

    while True:
        print(f"... Round: {game_round}")
        # Monsterbewegung
        for mi in Game.zoo:
            mi.ai()  # Möglichkeit das keine bewegung durchgeführt wird muss implementiert werden

        dungeon_string = print_dungeon()
        #print(f"Hero befindet sich an x: {hero.x},y: {hero.y}")
        event, values = window.read()
        window["dungeon"].update(dungeon_string)
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event in ("up", "down", "right", "left", "wait"):
            hero.bewegung( event)

        dungeon_string = print_dungeon()
        window["dungeon"].update(dungeon_string)

        # Entfernen der toten Monster aus dem Dungeon, manipuliert den current Level in der Funktion
        alive()

        #Ausgangsbedingung, der Hero muss leben
        if hero.hp <= 0:
            break

        game_round += 1
    # Finish up by removing from the screen
    window.close()


if __name__=="__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
    #main(sys)

            
            