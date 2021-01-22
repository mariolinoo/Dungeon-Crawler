from roll import wurfel
import PySimpleGUI as sg
sg.SetOptions(font = ("arial", 12))


def strike(attacker, defender):
    to_hit, to_hit_string = wurfel(attacker.to_hit)
    to_defend, to_defend_string = wurfel(defender.to_defense)
    dmg, dmg_string = wurfel(attacker.dmg)
    prot, prot_string = wurfel(defender.protection)
    print \
        (f"{attacker.name} swings with {to_hit_string} at {defender.name} with defense chance {to_defend_string}")
    if to_defend >= to_hit:
        print("Attack failed")
        return
    print \
        (f"{attacker.name} hits with {dmg_string} {defender.name} with {prot_string} armor")
    if dmg <= prot:
        print("No damage")
        return
    dmg -= prot
    defender.hp -= dmg
    print(f"{defender.name} looses {dmg}hp and has {defender.hp}hp left")


def fight(attacker, defender):
    strike(attacker, defender)
    if defender.hp <= 0:
        print(f"{defender.name} is dead")
        return
    print("Counterstrike")
    strike(defender, attacker)
    if attacker.hp <= 0:
        print(f"{attacker.name} is dead")

class Game:
    """Container für globale Variablen"""
    zoo = []  # Monsterliste
    graveyard = []
    current_level = []


class Monster:
    """Generic Monsterclass"""
    #Classatribute
    number=0 #Monsterid

    def __init__(self, gui_number=0): #self ist durch constructor definiert und kann beliebig gewählt werden
        self.number=Monster.number
        Monster.number+=1
        Game.zoo.append(self)
        self.gui_number = gui_number
        self.name = "nix"
        self.to_hit="1d2"
        self.dmg="1D5"
        self.to_defense="1D2"
        self.protection="1d2"
        #self.get_attributes_from_gui()
        self.post_init()

    def get_attributes_from_gui(self):
        """get attributes from left gui (self.gui-number ==0) or from right gui (self.gui-number==1)"""
        prefix = "a_" if self.gui_number == 0 else "b_"
        for fieldname in ["name",
                          "hp",
                          "to_hit",
                          "dmg",
                          "to_defend",
                          "protection",
                          ]:
            #print("processing:", fieldname)
            #print("value:", GUI.values)
            self.__setattr__(fieldname, GUI.values[prefix+fieldname])
        print("fertig!")
        #print("self dict")
        #print(self.__dict__)


    def post_init(self):
        pass



class GUI():
    window = None
    column_size = (600,400)
    button_size = (7,2)
    input_bar_size = (26,1)
    enter_text_size = (35,1)
    values = None
    monster_classes = [
            ["Alice", 10, "1d3+0","1d3+0","1d3+0","1d3+0"],
            ["Bob", 10, "1d3+0", "1d3+0", "1d3+0", "1d3+0"],
    ]


def main(duell=True):
    #alice=Alice()
    #bob=Bob()
    Monster(gui_number=0)
    Monster(gui_number=1)
    for m in Game.zoo:
        print(m, m.__dict__)


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
                        [sg.Button("pull values\nfrom table", key="pull_left", size=GUI.button_size)],
                        [sg.Button("push values\nto table", key="push_left", size=GUI.button_size)],
                    ], size = GUI.column_size
                    )

    middle = sg.Column  (
                        [

                            [sg.Text("Statistik kommt hier her")],
                            [sg.Text("defined monsters:")],
                            [sg.Table(values=GUI.monster_classes,
                                      headings=["name", "hp", "to_hit", "dmg", "to_defense", "protection"],
                                      auto_size_columns=False,
                                      col_widths=[15, 5, 5, 5,  5, 5],
                                      display_row_numbers=True,
                                      vertical_scroll_only=True,
                                      size=(70, 20),
                                      alternating_row_color= "#AAAAAA",
                                      justification="left",
                                      enable_events=True,
                                      select_mode = sg.TABLE_SELECT_MODE_BROWSE,
                                      #select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                                      key="monsters"),
                             ],


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
                            [sg.Button("pull values\nfrom table", key="pull_right", size=GUI.button_size)],
                            [sg.Button("push values\nto table", key="push_right", size=GUI.button_size)],

                        ], size=GUI.column_size
    )
    layout =    [
                    [left, middle, right],
                    [sg.Output(size = (120, 20))],
                    [sg.Button("Push values", size=GUI.button_size)],
                    [sg.Button("Run", size = GUI.button_size), sg.Cancel(size = GUI.button_size), sg.Button("save table\nto monsters.csv", key="save_table", size=GUI.button_size)],
                ]

    GUI.window = sg.Window('fight_simulator', layout)
    GUI.window.finalize()
    #GUI.values = GUI.window.read()[1]

    while True:
        event, values = GUI.window.read()
        GUI.values = values
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "Push values":
            for m in Game.zoo:
                m.get_attributes_from_gui()
                print(m, m.__dict__)

        if event == "Run":
            if duell:
                alice = Game.zoo[0]
                bob = Game.zoo[1]
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