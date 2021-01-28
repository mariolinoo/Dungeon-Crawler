from roll import wurfel
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib

matplotlib.use('TKAgg')

sg.SetOptions(font = ("arial", 12))

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
        self.hp = 10
        self.gui_number = gui_number
        self.name = "nix"
        self.to_hit="1d2"
        self.dmg="1D5"
        self.to_defend="1D2"
        self.protection="1d2"
        self.initiative="1d2"
        self.reset_stat()

    def get_attributes_from_gui(self):
        prefix = "a_" if self.gui_number == 0 else "b_"

        for suffix in   [
                            "name",
                            "hp",
                            "to_hit",
                            "dmg",
                            "to_defend",
                            "protection",
                        ]:
            self.__setattr__(suffix, GUI.values[prefix + suffix])

        #print(self.__dict__)

    def reset_stat(self):
        self.stat_dict = {"hit": 0, "miss": 0, "penetration": 0, "no_penetration": 0, "first_strike":0,
                          "second_strike":0, "got_hit": 0, "evaded": 0, "armor_penetrated": 0,
                          "successfull_block": 0}
        self.hp_list = []
        self.dmg_dealt_list = []
        self.dmg_recieved_list = []

class GUI:
    window = None
    column_size = (450,650)
    button_size = (7,2)
    extended_menue_button_size = (1, 1)
    input_bar_size = (15,1)
    enter_text_size = (25,1)
    values = None
    monster_classes = [
            ["Alice", 10, "1d3+0","1d3+0","1d3+0","1d3+0"],
            ["Bob", 10, "1d3+0", "1d3+0", "1d3+0", "1d3+0"],
    ]

def draw_figure(canvas, figure):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side = 'top', fill = 'both', expand = 1)

    return figure_canvas_agg

def line_plot(fighterA, fighterB, titlestring, xinch = 5, yinch = 5, res = 100):
    print(f"{fighterA.name} dmg list: {fighterA.dmg_dealt_list}")
    print(f"{fighterB.name} dmg list: {fighterB.dmg_dealt_list}")

    """create a line plot diagramm"""
    fi, ax = plt.subplots(figsize = (xinch, yinch), dpi = res)
    if len(fighterA.hp_list) != len(fighterB.hp_list):
        raise ValueError(f"hp list from {fighterA.name} must have the same lenght as hp list from {fighterB.name}")
    if len(fighterA.dmg_dealt_list) != len(fighterB.dmg_dealt_list):
        raise ValueError(f"dmg list from {fighterA.name} must have the same lenght as dmg list from {fighterB.name}")
    t = range(len(fighterA.hp_list))
    ax.plot(t, fighterA.hp_list, label = f"{fighterA.name} hp")
    ax.plot(t, fighterB.hp_list, label = f"{fighterB.name} hp")
    ax.plot(t, fighterA.dmg_dealt_list, label = f"{fighterA.name} dmg")
    ax.plot(t, fighterB.dmg_dealt_list, label = f"{fighterB.name} dmg")
    ax.legend()
    ax.grid()
    ax.set(title = titlestring, xlabel = "All combatrounds", ylabel = "hp and dmg")
    ax.axhline(y=0, color = 'r', linestyle = 'dashed', linewidth = 2)
    fig = plt.gcf()
    return fig

def append_stats(fighterA, fighterB, dmg_a, dmg_b):
    fighterA.dmg_dealt_list.append(dmg_a)
    fighterB.dmg_dealt_list.append(dmg_b)
    fighterB.dmg_recieved_list.append(dmg_b)
    fighterB.dmg_recieved_list.append(dmg_a)
    fighterA.hp_list.append(fighterA.hp)
    fighterB.hp_list.append(fighterB.hp)


def strike(attacker, defender):
    to_hit, to_hit_string = wurfel(attacker.to_hit)
    to_defend, to_defend_string = wurfel(defender.to_defend)
    dmg, dmg_string = wurfel(attacker.dmg)
    prot, prot_string = wurfel(defender.protection)

    print(f"{attacker.name} swings with {to_hit_string} at {defender.name} with defense chance {to_defend_string}")
    if to_defend >= to_hit:
        attacker.stat_dict["miss"] += 1
        defender.stat_dict["evaded"] += 1
        append_stats(attacker, defender, 0, 0)
        print("Attack failed")
        return

    attacker.stat_dict["hit"] += 1
    defender.stat_dict["got_hit"] += 1
    print(f"{attacker.name} hits with {dmg_string} {defender.name} with {prot_string} armor")
    if dmg <= prot:
        print("No damage")
        attacker.stat_dict["no_penetration"] += 1
        defender.stat_dict["successfull_block"] += 1
        append_stats(attacker, defender, 0, 0)
        return

    attacker.stat_dict["penetration"] += 1
    defender.stat_dict["armor_penetrated"] += 1

    dmg -= prot
    defender.hp -= dmg

    append_stats(attacker, defender, dmg, 0)

    print(f"{defender.name} looses {dmg}hp and has {defender.hp}hp left")

def fight(fighter_a, fighter_b):
    init_a, init_b = 0, 0

    while (init_a == init_b):
        init_a = wurfel(fighter_a.initiative)
        init_b = wurfel(fighter_b.initiative)

    if init_a > init_b:
        fighter_a.stat_dict["first_strike"] += 1
        fighter_b.stat_dict["second_strike"] += 1
        attacker, defender = fighter_a, fighter_b
    else:
        fighter_b.stat_dict["first_strike"] += 1
        fighter_a.stat_dict["second_strike"] += 1
        attacker, defender = fighter_b, fighter_a

    print(attacker.name, "strikes first")

    strike(attacker, defender)
    if defender.hp <= 0:
        print(f"{defender.name} is dead")
        return
    print("Counterstrike")
    strike(defender, attacker)
    if attacker.hp <= 0:
        print(f"{attacker.name} is dead")
        return

def string_constructor(dd):

    string = ""
    string = str(dd["dice"])
    string += "D" if dd["reroll"] else "d"
    string += str(dd["sides"])
    string += "+" if dd["correction"] > 0 else "-"
    string += str(abs(dd["correction"]))

    return string

def dice_parameters(prefix, suffix):

    layout_pop = [
                    [sg.Text("Number of dice")],
                    [sg.Slider([0, 100], orientation="h", default_value=10, resolution=1,
                               size=(22, 15), key="dice_dice", enable_events=True)],

                    [sg.Text("")],
                    [sg.Checkbox(text="Reroll", key="dice_reroll", size=GUI.button_size
                                 , enable_events=True)],
                    [sg.Text("")],

                    [sg.Text("Sides per die")],
                    [sg.Slider([2, 100], orientation="h", default_value=10, resolution=1,
                               size=(22, 15), key="dice_sides", enable_events=True)],

                    [sg.Text("Bonus value")],
                    [sg.Slider([-100, 100], orientation="h", default_value=10, resolution=1,
                               size=(22, 15), key="dice_correction", enable_events=True)],

                    [sg.Text("", font=("arial", 24), key="dice_result", size=(15, 1))],

                    [sg.Ok(size=GUI.button_size), sg.Cancel(size=GUI.button_size)],
                ]

    name = GUI.values[prefix + suffix]
    dd = {}
    dd["dice"], dd["reroll"], dd["sides"], dd["correction"] = wurfel(name, data = True)

    window_pop = sg.Window('dice_constructor', layout_pop)

    window_pop.finalize()

    for suffix in dd.keys():
        string = "dice_" + suffix
        window_pop[string].Update(value = dd[suffix])

    while True:
        event, values = window_pop.read()

        for suffix in dd.keys():
            string = "dice_" + suffix
            dd[suffix] = int(values[string])

        dice_string = string_constructor(dd)

        print(dice_string)

        window_pop["dice_result"].Update(dice_string)

        if event == sg.WIN_CLOSED or event == "Cancel":
            break

        if event == "Ok":
            window_pop.close()
            return dice_string

    window_pop.close()

    return

def pull_fighter_from_table(side):
    prefix = "a_" if side == "a" else "b_"
    # überprüfuen ob im table etwas selektiert ist
    if len(GUI.values["monsters"]) == 0:
        sg.popup_ok("select a monster in the list first")
        return
    selected_row = GUI.values["monsters"][0]  # zeilennummer
    print(selected_row)
    fieldnames = ["name", "hp", "to_hit", "dmg", "to_defend", "protection"]
    for i, field in enumerate(fieldnames):
        print(GUI.monster_classes[selected_row][i])
        GUI.window[prefix + field].update(GUI.monster_classes[selected_row][i])

def push_fighter_to_table(side):
    prefix = "a_" if side == "a" else "b_"
    fieldnames = ["name", "hp", "to_hit", "dmg", "to_defend", "protection"]
    # überprüfen ob name schon in tabelle drin ist
    myname = GUI.values[prefix + "name"]
    already_inside = False
    for y, line in enumerate(GUI.monster_classes):
        if line[0] == myname:
            already_inside = True
            print("found it in table")
            break  # found name, it's already in table
    else:  # never have breaked out of loop
        print("did not found in table")
        already_inside = False
    # update monster_classes
    if already_inside:
        for i, field in enumerate(fieldnames):
            # print("y,i, field", y, i, field)
            # print("zeile:", GUI.monster_classes[y])
            # print("form-value:", values[prefix+field])
            if type(GUI.monster_classes[y][i]) != str:
                new_value = int(GUI.values[prefix + field])
            else:
                new_value = GUI.values[prefix + field]
            GUI.monster_classes[y][i] = new_value
    else:
        append_list = []
        for x, field in enumerate(fieldnames):
            if type(GUI.values[prefix + field]) == str:
                append_list.append(GUI.values[prefix + field])
            else:
                append_list.append(int(GUI.values[prefix + field]))

        GUI.monster_classes.append(append_list)

    # update table element
    GUI.window["monsters"].Update(GUI.monster_classes)

def def_layout():

    left = sg.Column([
        [sg.Text("Enter name:", size=GUI.enter_text_size),
         sg.Input(default_text="Alice", key="a_name", size=GUI.input_bar_size)],

        [sg.Text("Enter hp:", size=GUI.enter_text_size),
         sg.Slider([1, 100], orientation="h", default_value=10, resolution=1,
                   size=(15, 15), key="a_hp")],

        [sg.Text("Enter (dice) hit possibility:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="a_to_hit", size=GUI.input_bar_size),
         sg.Button("...", key="a_to_hit_dice", size=GUI.extended_menue_button_size)],

        [sg.Text("Enter (dice) damage:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="a_dmg", size=GUI.input_bar_size),
         sg.Button("...", key="a_dmg_dice", size=GUI.extended_menue_button_size)],

        [sg.Text("Enter (dice) defense possibility:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="a_to_defend", size=GUI.input_bar_size),
         sg.Button("...", key="a_to_defend_dice", size=GUI.extended_menue_button_size)],

        [sg.Text("Enter (dice) protection:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="a_protection", size=GUI.input_bar_size),
         sg.Button("...", key="a_protection_dice", size=GUI.extended_menue_button_size)],

        [sg.Text("Enter (dice) initiative:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="a_initativ", size=GUI.input_bar_size),
         sg.Button("...", key="a_initativ_dice", size=GUI.extended_menue_button_size)],

        [sg.Button("pull values\nfrom table", key="pull_a", size=GUI.button_size),
         sg.Button("push values\nto table", key="push_a", size=GUI.button_size)],

        [sg.Text("Enter name:", size=GUI.enter_text_size),
         sg.Input(default_text="Bob", key="b_name", size=GUI.input_bar_size)],

        [sg.Text("Enter hp:", size=GUI.enter_text_size),
         sg.Slider([1, 100], orientation="h", default_value=10, resolution=1,
                   size=(15, 15), key="b_hp")],

        [sg.Text("Enter (dice) hit possibility:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="b_to_hit", size=GUI.input_bar_size),
         sg.Button("...", key="b_to_hit_dice", size=GUI.extended_menue_button_size)],

        [sg.Text("Enter (dice) damage:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="b_dmg", size=GUI.input_bar_size),
         sg.Button("...", key="b_dmg_dice", size=GUI.extended_menue_button_size)],

        [sg.Text("Enter (dice) defense possibility:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="b_to_defend", size=GUI.input_bar_size),
         sg.Button("...", key="b_to_defend_dice", size=GUI.extended_menue_button_size)],

        [sg.Text("Enter (dice) protection:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="b_protection", size=GUI.input_bar_size),
         sg.Button("...", key="b_protection_dice", size=GUI.extended_menue_button_size)],

        [sg.Text("Enter (dice) initiative:", size=GUI.enter_text_size),
         sg.Input(default_text="1d6+0", key="b_initativ", size=GUI.input_bar_size),
         sg.Button("...", key="b_initativ_dice", size=GUI.extended_menue_button_size)],

        [sg.Button("pull values\nfrom table", key="pull_b", size=GUI.button_size),
         sg.Button("push values\nto table", key="push_b", size=GUI.button_size)],

    ], size=GUI.column_size)

    middle = sg.Column([
        [sg.Text("defined monsters:")],
        [sg.Table(values=GUI.monster_classes,
                  headings=["name", "hp", "to_hit", "dmg", "to_defend", "protection"],
                  auto_size_columns=False,
                  col_widths=[15, 4, 7, 7, 7, 7],
                  display_row_numbers=True,
                  vertical_scroll_only=True,
                  size=(80, 30),
                  alternating_row_color="#AAAAAA",
                  justification="left",
                  enable_events=True,
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                  key="monsters"), ],
    ], size = (600,650), vertical_alignment = "top")

    lower_right_column = sg.Column([
        [sg.Text("Number of duells: "),
         sg.Slider([1, 100], orientation="h", default_value=0, resolution=1, size=(22, 15), key="fights"),
         sg.Text("Fights per duell: "),
         sg.Slider([0, 100], orientation="h", default_value=0, resolution=1, size=(22, 15), key="game_rounds",
                   enable_events=True),
         sg.Text("to the death", key="game_round_text", size=(20, 1)), ],

        [sg.Button("Fight", size=GUI.button_size), sg.Cancel(size=GUI.button_size),
         sg.Button("save table\nto .csv", key="save_table", size=GUI.button_size),
         sg.Button("load table\nfrom .csv", key="load_table", size=GUI.button_size),
         sg.Button("Delete table", key="delete_table", size=GUI.button_size),
         sg.Button("Delete\n entry", key="delete_entry", size=GUI.button_size), ],
    ])

    diagrams = sg.Column([
        [sg.Canvas(key="CANVAS1"), ],
    ], vertical_alignment = "top")

    return left, middle, lower_right_column, diagrams

def main():
    #ToDo Statistische Auswertung der Kämpfe, Initivwert für Kämpfer, eigenes Programm für Kämpfe

    # Definition des GUI Layouts
    left, middle, lower_right_column, diagrams = def_layout()

    layout_command = sg.Column([
        [left, middle],
        [lower_right_column],
    ])

    layout = [
        [layout_command, diagrams]
    ]

    GUI.window = sg.Window('main_window', layout)

    fighterA = Monster(gui_number=0)
    fighterB = Monster(gui_number=1)

    while True:

        #Auslesen der durch das Fenster generierten Events und die Werte der Eingaben
        event, values = GUI.window.read()
        #Abspeichern der Werte aus dem GUI für den globalen gebrauch
        GUI.values = values

        #Wird Cancel gedrückt oder das Fenster manuell geschlossen
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

        #Startet einen Kampf nach den definierten Parameter
        if event == "Fight":
            #Abstand in der Ausgabe um Kämpfe unterscheiden zu können
            for i in range(40):
                print("")

            print("Fight")
            #Battle
            fighterA = Game.zoo[0]
            fighterB = Game.zoo[1]
            fighterA.reset_stat()
            fighterB.reset_stat()
            fighterA.get_attributes_from_gui()
            fighterB.get_attributes_from_gui()
            battle_round = 0
            max_rounds = GUI.values["game_rounds"]
            fighterA.hp_list.append(fighterA.hp)
            fighterB.hp_list.append(fighterB.hp)
            fighterA.dmg_dealt_list.append(0)
            fighterB.dmg_dealt_list.append(0)
            fighterA.dmg_recieved_list.append(0)
            fighterB.dmg_recieved_list.append(0)
            GUI.window["fights"].Update(disabled = True)

            for i in range(int(GUI.values["fights"])):
                fighterA.get_attributes_from_gui()
                fighterB.get_attributes_from_gui()
                while True:
                    battle_round += 1
                    if fighterA.hp <= 0 or fighterB.hp <= 0:
                        break
                    if max_rounds != 0 and max_rounds != 100:
                        if battle_round > max_rounds:
                            print("Battle ended by round limit")
                            break
                    print(f"Battle round : {battle_round}")

                    fight(fighterA, fighterB)

            GUI.window["fights"].Update(disabled = False)
            fig_fight_hp = line_plot(fighterA, fighterB, "hp and dmg over time", 7.5, 3.75, 100)
            fig_canvas_agg = draw_figure(GUI.window['CANVAS1'].TKCanvas, fig_fight_hp)

            if fighterA.hp == fighterB.hp:
                print("Draw")
            elif fighterA.hp > fighterB.hp:
                print(fighterA.name, " won")
            else:
                print(fighterB.name, " won")

        #Pull left and right zieht aus der Haupttabelle einen Kämpfer in die entsprechende Position
        if event == "pull_a":
            pull_fighter_from_table("a")

        if event == "pull_b":
            pull_fighter_from_table("b")

        #Push left und right speichert den zusammengestellten Kämper aus der entsprechenden Position in der Tabelle ab
        if event == "push_a":
            push_fighter_to_table("a")

        if event == "push_b":
            push_fighter_to_table("b")

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

        if event == "delete_entry":
            # überprüfuen ob im table etwas selektiert ist
            if len(values["monsters"]) == 0:
                sg.popup_ok("select a monster in the list first")
                continue

            print(values["monsters"][0])

            GUI.monster_classes.pop(values["monsters"][0])
            GUI.window["monsters"].Update(GUI.monster_classes)

        for prefix in ["a_", "b_", ]:
            for suffix in ["to_hit", "to_defend", "dmg", "protection", "initativ"]:
                compare_string = prefix + suffix + "_dice"
                if event == compare_string:
                    GUI.window[prefix + suffix].Update(dice_parameters(prefix, suffix))

        if event == "game_rounds":
            if int(values["game_rounds"]) in (0,100):
                GUI.window["game_round_text"].Update("to the death")
            else:
                GUI.window["game_round_text"].Update("rounds")

    GUI.window.close()


if __name__=="__main__":
    main()