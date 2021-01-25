from roll import wurfel
import PySimpleGUI as sg
sg.SetOptions(font = ("arial", 12))


def strike(attacker, defender):
    to_hit, to_hit_string = wurfel(attacker.to_hit)
    to_defend, to_defend_string = wurfel(defender.to_defense)
    dmg, dmg_string = wurfel(attacker.dmg)
    prot, prot_string = wurfel(defender.protection)
    print(f"{attacker.name} swings with {to_hit_string} at {defender.name} with defense chance {to_defend_string}")
    if to_defend >= to_hit:
        print("Attack failed")
        return
    print(f"{attacker.name} hits with {dmg_string} {defender.name} with {prot_string} armor")
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

    def post_init(self):
        pass



class GUI():
    window = None
    column_size = (600,400)
    button_size = (7,2)
    extended_menue_button_size = (1, 1)
    input_bar_size = (26,1)
    enter_text_size = (25,1)
    values = None
    monster_classes = [
            ["Alice", 10, "1d3+0","1d3+0","1d3+0","1d3+0"],
            ["Bob", 10, "1d3+0", "1d3+0", "1d3+0", "1d3+0"],
    ]


def main(duell=True):
    #ToDo Statistische Auswertung der Kämpfe, Dice zusammenstellen,
    #alice=Alice()
    #bob=Bob()
    Monster(gui_number=0)
    Monster(gui_number=1)
    for m in Game.zoo:
        print(m, m.__dict__)


    left = sg.Column(
                    [
                        [sg.Text("Enter name:", size = GUI.enter_text_size),
                         sg.Input(default_text = "Alice", key = "a_name", size = GUI.input_bar_size)],
                        [sg.Text("Enter hp:", size = GUI.enter_text_size),
                         sg.Slider([1, 100], orientation="h", default_value=10, resolution=1,
                                   size=(22, 15), key="a_hp")],
                        [sg.Text("Enter (dice) hit possibility:", size = GUI.enter_text_size),
                         sg.Input(default_text="1d6+0", key="a_to_hit", size=GUI.input_bar_size),
                         sg.Button("...", key="left_hit_dice", size = GUI.extended_menue_button_size)],
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
                                      col_widths=[15, 4, 7, 7,  7, 7],
                                      display_row_numbers=True,
                                      vertical_scroll_only=True,
                                      size=(80, 20),
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
                             sg.Input(default_text="Bob", key="b_name", size=GUI.input_bar_size)],
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
                    #[sg.Output(size = (120, 20))],
                    [sg.Button("Run", size = GUI.button_size), sg.Cancel(size = GUI.button_size), sg.Button("save table\nto .csv", key="save_table", size=GUI.button_size),
                     sg.Button("load table\nfrom .csv", key="load_table", size=GUI.button_size), sg.Button("Delete table", key="delete_table", size=GUI.button_size),
                     sg.Button("Delete\n entrie", key="delete_entrie", size=GUI.button_size)],
                ]

    layout_pop =    [
                        [sg.Text("Number of dice")],
                        [sg.Slider([1, 100], orientation="h", default_value = 10, resolution=1,
                                       size=(22, 15), key="dice_nr")],
                        [sg.Text("Sides per die")],
                        [sg.Slider([1, 100], orientation="h", default_value = 10, resolution=1,
                                       size=(22, 15), key="dice_sides")],
                        [sg.Text("Bonus value")],
                        [sg.Slider([1, 100], orientation="h", default_value = 10, resolution=1,
                                       size=(22, 15), key="dice_bonus")],

                        [sg.Text("Your dice is: .....", font = ("arial", 24), key  = "dice_result")],

                        [sg.Ok(size = GUI.button_size), sg.Cancel(size = GUI.button_size), sg.Button("Update", key = "update_dice", size = GUI.button_size)],

                    ]

    GUI.window = sg.Window('fight_simulator', layout)
    GUI.window.finalize()
    #GUI.values = GUI.window.read()[1]

    while True:
        event, values = GUI.window.read()
        GUI.values = values
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

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

        if event in ( "pull_left", "pull_right"):
            prefix = "a_" if event == "pull_left" else "b_"
            # überprüfuen ob im table etwas selektiert ist
            if len(values["monsters"]) == 0:
                sg.popup_ok("select a monster in the list first")
                continue
            selected_row = values["monsters"][0] # zeilennummer
            print(selected_row)
            fieldnames = ["name", "hp", "to_hit", "dmg", "to_defend", "protection"]
            for i, field in enumerate(fieldnames):
                print(GUI.monster_classes[selected_row][i])
                GUI.window[prefix+field].update(GUI.monster_classes[selected_row][i])

        if event in ("push_left", "push_right"):
            prefix = "a_" if event == "push_left" else "b_"
            fieldnames = ["name", "hp", "to_hit", "dmg", "to_defend", "protection"]
            # überprüfen ob name schon in tabelle drin ist
            myname = values[prefix+"name"]
            already_inside = False
            for y, line in enumerate(GUI.monster_classes):
                if line[0] == myname:
                    already_inside = True
                    print("found it in table")
                    break # found name, it's already in table
            else:  # never have breaked out of loop
                print("did not found in table")
                already_inside = False
            # update monster_classes
            if already_inside:
                for i, field in enumerate(fieldnames):
                    #print("y,i, field", y, i, field)
                    #print("zeile:", GUI.monster_classes[y])
                    #print("form-value:", values[prefix+field])
                    if type(GUI.monster_classes[y][i]) != str:
                        new_value = int(values[prefix+field])
                    else:
                        new_value = values[prefix+field]
                    GUI.monster_classes[y][i] = new_value
            else:
                append_list = []
                for x,field in enumerate(fieldnames):
                    if type(values[prefix + field]) == str:
                        append_list.append(values[prefix + field])
                    else:
                        append_list.append(int(values[prefix + field]))

                GUI.monster_classes.append(append_list)

            # update table element
            GUI.window["monsters"].Update(GUI.monster_classes)

        if event == "load_table":
            load_file = sg.popup_get_file("Please select file to load in to the monster table")
            print(load_file)

            with open (load_file, "r") as f:
                GUI.monster_classes = []
                for line in f:
                    clean_line = []
                    for x,field in enumerate(line.split(",")):
                        if x != 1:
                            clean_line.append(field.strip()[1:-1])

                        else:
                            clean_line.append(int(field.strip()))
                    GUI.monster_classes.append(clean_line)

            GUI.window["monsters"].Update(GUI.monster_classes)


        if event == "save_table":
            save_cmd = sg.popup_yes_no("Save to the default file?")

            #Standard file
            save_filename = "standard_table.csv"

            #Auswahl des eigenene files
            if save_cmd == "No":
                sg.popup_notify("You have to create the file on your own")
                # Überschreibt den standardfile, falls eigenes ausgesucht wird
                save_filename = sg.popup_get_file("Please select or create file for monster table (.csv format)")
                if save_filename is None:
                    sg.PopupOK("Incorrect file description")
                    continue
            #Öffnen des Files und abspeichern der Tabelle
            with open (save_filename, "w") as f:
                for line in GUI.monster_classes:
                    for field in line:
                        if type(field) is str:
                            f.write("'"+field+"'") #csv dateien brauchen strings in single quotes
                        else:
                            f.write(str(field))
                        f.write(",")
                    f.write("\n")

        if event == "delete_table":
            GUI.monster_classes = []
            GUI.window["monsters"].Update(GUI.monster_classes)

        if event == "delete_entrie":
            # überprüfuen ob im table etwas selektiert ist
            if len(values["monsters"]) == 0:
                sg.popup_ok("select a monster in the list first")
                continue

            print(values["monsters"][0])

            GUI.monster_classes.pop(values["monsters"][0])
            GUI.window["monsters"].Update(GUI.monster_classes)











if __name__=="__main__":
    main()