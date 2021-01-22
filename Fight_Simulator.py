from roll import wurfel
import PySimpleGUI as sg
sg.SetOptions(font = ("arial", 12))


def strike(attacker, defender):
    to_hit, to_hit_string = wurfel(attacker.to_hit_dice)
    to_defend, to_defend_string = wurfel(defender.to_defense_dice)
    dmg, dmg_string = wurfel(attacker.dmg_dice)
    prot, prot_string = wurfel(defender.protection_dice)
    print \
        (f"{attacker.__class__.__name__} swings with {to_hit_string} at {defender.__class__.__name__} with defense chance {to_defend_string}")
    if to_defend >= to_hit:
        print("Attack failed")
        return
    print \
        (f"{attacker.__class__.__name__} hits with {dmg_string} {defender.__class__.__name__} with {prot_string} armor")
    if dmg <= prot:
        print("No damage")
        return
    dmg -= prot
    defender.hp -= dmg
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
        self.post_init()

    def post_init(self):
        pass

class Bob(Monster):

    def post_init(self):
        self.to_hit_dice = "1d2"
        self.dmg_dice = "1D5"
        self.to_defense_dice = "1D2"
        self.protection_dice = "1d2"
        self.hp = 50

class Alice(Monster):

    def post_init(self):
        self.to_hit_dice = "1d2"
        self.dmg_dice = "1D5"
        self.to_defense_dice = "1D2"
        self.protection_dice = "1d2"
        self.hp = 40

class GUI():
    window = None
    column_size = (600,400)
    button_size = (7,2)
    input_bar_size = (26,1)
    enter_text_size = (35,1)


def main(duell=True):
    alice=Alice()
    bob=Bob()

    left = sg.Column(
                    [
                        [sg.Text("Enter name:", size = GUI.enter_text_size),
                         sg.Input(default_text = "alice", key = "a_name", size = GUI.input_bar_size)],
                        [sg.Text("Enter hp:", size = GUI.enter_text_size),
                         sg.Slider([1, 100], orientation="h", default_value=10, resolution=1,
                                   size=(22, 15), key="a_hp")],
                        [sg.Text("Enter (dice) hit possibility:", size = GUI.enter_text_size),
                         sg.Input(default_text="1d6+0", key="a_to_hit", size=GUI.input_bar_size)],
                        [sg.Text("Enter (dice) damage:", size = GUI.enter_text_size),
                         sg.Input(default_text="1d6+0", key="a_dmg", size=GUI.input_bar_size)],
                        [sg.Text("Enter (dice) defense possibility:", size = GUI.enter_text_size),
                         sg.Input(default_text="1d6+0", key="a_to_defend", size=GUI.input_bar_size)],
                        [sg.Text("Enter (dice) protection:", size = GUI.enter_text_size),
                         sg.Input(default_text="1d6+0", key="a_protection", size=GUI.input_bar_size)],
                    ], size = GUI.column_size
                    )

    middle = sg.Column  (
                        [
                            [sg.Text("Statistik kommt hier her")],
                        ], size = GUI.column_size
                        )
    right = sg.Column  (
                        [
                            [sg.Text("Enter name:", size=GUI.enter_text_size),
                             sg.Input(default_text="bob", key="b_name", size=GUI.input_bar_size)],
                            [sg.Text("Enter hp:", size=GUI.enter_text_size),
                             sg.Slider([1, 100], orientation="h", default_value = 10, resolution=1,
                                       size=(22, 15), key="b_hp")],
                            [sg.Text("Enter (dice) hit possibility:", size=GUI.enter_text_size),
                             sg.Input(default_text="1d6+0", key="b_to_hit", size=GUI.input_bar_size)],
                            [sg.Text("Enter (dice) damage:", size=GUI.enter_text_size),
                             sg.Input(default_text="1d6+0", key="b_dmg", size=GUI.input_bar_size)],
                            [sg.Text("Enter (dice) defense possibility:", size=GUI.enter_text_size),
                             sg.Input(default_text="1d6+0", key="b_to_defend", size=GUI.input_bar_size)],
                            [sg.Text("Enter (dice) protection:", size=GUI.enter_text_size),
                             sg.Input(default_text="1d6+0", key="b_protection", size=GUI.input_bar_size)],

                        ], size=GUI.column_size
    )
    layout =    [
                    [left, middle, right],
                    [sg.Output(size = (120, 20))],
                    [sg.Button("Run", size = GUI.button_size), sg.Cancel(size = GUI.button_size)],
                ]

    GUI.window = sg.Window('fight_simulator', layout)
    GUI.window.finalize()

    while True:
        event, values = GUI.window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Run":
            if duell:
                while (alice.hp > 0 and bob.hp > 0):
                    fight(alice, bob)
                if alice.hp > 0:
                    print("Alice won")
                else:
                    print("Bob won")
            else:
                fight(alice, bob)



if __name__=="__main__":
    main()