# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Matplotlib.py
import PySimpleGUI as sg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import numpy as np
import matplotlib

matplotlib.use('TKAgg') # important for dicethrow function!

#rng = np.random.default_rng() # only when using numpy instead of random module


class Player:

    def __init__(self, name, hp, attack, defense, damage, protection):
        self.name = name
        self.hp = int(hp)
        self.hp_full = int(hp)
        self.attack = attack
        self.defense = defense
        self.damage = damage
        self.protection = protection

    def heal(self):
        self.hp = self.hp_full


def dicethrow(dice=1, reroll=True, sides=6, correction=0):
    """returns the sum of dice throws, the sides begin with number 1
       if a 6 (or hightest side number) is rolled AND reroll==True,
       then sides-1 is counted and another roll is made and added
       (can be repeated if another 6 is rolled).
       example:
       roll 5 -> 5
       roll 6, reroll 1 -> 5+1 = 6
       roll 6, reroll 6, reroll 3 -> 5 + 5 + 3 = 13
       correction is added (subtracted) to the end sum, after all rerolls
       important:
       expecting random module imported in this module
       ##expect rng = np.random.default_rng() declared before call
    """
    total = 0
    for d in range(dice):
        #roll = rng.integers(1,sides,1, endpoint=True)
        roll = random.randint(1, sides)
        ##print(roll)
        if not reroll:
            ##total += roll[0]
            total += roll
        elif roll < sides:
            ##total+=roll[0]
            total += roll
        else:
            #print("re-rolling...")
            total += sides - 1
            total += dicethrow(1, reroll,  sides) # + correction already here??
    return total + correction


def dice_from_string(dicestring="1d6"):
    """expecting a dicestring in the format:
       {dice}d{sides}+{correction}
       examples:
       1d6+0 ... one 6 sided die without re-roll
       2D6+0 ... two 6-sided dice with reroll
       1d20+1 ... one 20-sided die, correction value +1
       3D6-2 ... three 6-sided dice with reroll, sum has correction value of -2
       where:
       d........means dice without re-roll
       D........means dice with re-roll (1D6 count as 5 + the reroll value)
       {dice} ...means number of dice throws, 2d means 2 dice etc. the sum of all throws is returned. must be integer
       {sides} ...means mumber of sides per die dice. d20 means 20-sided dice etc. must be integer
       {correction}.......means correction value that is added (subtracted) to the sum of all throws. must be integer

       returns [dice, recroll, sides, correction] and None when string is correct
       returns [None, None, None, None] and Errormessage when string is not correct
       """
    # checking if string is correct
    dicestring = dicestring.strip() # remove leading and trailing blanks
    if dicestring.lower().count("d") != 1:
        return [None,None,None,None], "none or more than one d (or D) found in: "+dicestring
    dpos = dicestring.lower().find("d")
    reroll = True if dicestring[dpos] == "D" else False
    try:
         dice = int(dicestring[:dpos])
    except ValueError:
        return [None,None,None,None], "integer value before d is missing in: " + dicestring
    rest = dicestring[dpos+1:]
    seperator = "+" if "+" in rest else ("-" if "-" in rest else None)
    if seperator is not None:
        try:
              sides = int(rest[:rest.find(seperator)])
        except ValueError:
            return [None,None,None,None], "integer value after d is missing in: " + dicestring
        try:
            correction = int(rest[rest.find(seperator):])
        except ValueError:
            return [None,None,None,None], "integer value afer + (or -) is missing in: " + dicestring
    else:
        try:
            sides = int(rest)
        except ValueError:
            return [None, None, None, None], "integer value after d is missing in: " + dicestring
        correction = 0
    #print("dice {} sides {} correction {}".format(dice, sides, correction))
    return [dice, reroll, sides, correction], None



def strike(a,b, verb="swings", show_dicestrings=True, show_starting_hp=True):
    """attacker strike at defender"""
    #print(dice_from_string(a.attack)[0])
    #return
    output = ""
    a_att = dicethrow(*dice_from_string(a.attack)[0])
    b_def = dicethrow(*dice_from_string(b.defense)[0])
    a_dam = dicethrow(*dice_from_string(a.damage)[0])
    b_prot = dicethrow(*dice_from_string(b.protection)[0])
    a_name = "{}{}".format(a.name, (" (" + str(a.hp) + "hp)") if show_starting_hp else "" )
    b_name = "{}{}".format(b.name, (" (" + str(b.hp) + "hp)") if show_starting_hp else "")
    if show_dicestrings:
        output += f"{a_name} {verb} at {b_name}, rolling {a.attack}={a_att} vs. {b.defense}={b_def}"
    else:
        output += f"{a_name} {verb} at {b_name}, rolling {a_att} vs. {b_def}"

    if a_att <= b_def:
        output +=" --> MISS\n"
        return output
    output += " --> HIT\n"
    if show_dicestrings:
        output += f"...damage of {a.damage}={a_dam} vs. protection of {b.protection}={b_prot}"
    else:
        output += f"...damage of {a_dam} vs. protection of {b_prot}"

    if a_dam <= b_prot:
        output += " --> NO DAMAGE\n"
        return output
    dam = a_dam - b_prot
    output += f" --> {dam} DAMAGE ({b.hp - dam} hp left)\n"
    b.hp -= dam
    return output

def fight(a,b):
    """strike and (if victim survives) counterstrike"""
    output = strike(a,b, "strikes")
    if b.hp > 0:
        output += strike(b,a, "counterstrikes")
    return output



def calculate(amount, dice, sides, reroll, corr):
    result = np.empty(amount)
    for i in range(amount):
        result[i] = dicethrow(dice, sides, reroll, corr)
    return result


def line_plot(dataA, dataB, titlestring, xinch=5, yinch=5, res=100,):
    """create a line plot diagram"""
    fi, ax = plt.subplots(figsize=(xinch, yinch), dpi=res) # inch x inch y, dpi
    if len(dataA) != len(dataB):
        raise ValueError("data A must have same length as data B")
    t = range(len(dataA))
    ax.plot(t, dataA, label="Player A")
    ax.plot(t, dataB, label="Player B")
    ax.legend()
    ax.grid()
    ax.set(title = titlestring, xlabel = "All combatrounds", ylabel="hp")
    ax.axhline(y=0, color='r', linestyle='dashed', linewidth=2)
    #rot = 0 if (len(dataA) < 20) else 90 # rotation of font in x-axis
    #plt.xticks(range(len(dataA) + 1, 1), rotation=rot)
    fig = plt.gcf()
    return fig

def histogram_plot(result, titlestring, xinch=5, yinch=5, res=100, zeroline=True):
    # plot histogram
    borders = np.arange(min(result)-0.25, max(result) + 0.3, 0.5)  # (left/right edges of bars in graph)
    fi, ax = plt.subplots(figsize=(xinch, yinch), dpi=res) # inch x inch y, dpi
    ax.hist(x=result, bins=borders)

    ax.set(title=titlestring,
           xlabel= "hp",
           ylabel="amount")
    if zeroline:
        ax.axvline(x=0, color='r', linestyle='dashed', linewidth=2)
    rot = 0 if ((max(result) - min(result)) < 10) else 90 # rotation of font in x-axis
    plt.xticks(np.arange(min(result), max(result) + 1, 1.0), rotation=rot)
    fig = plt.gcf()
    return fig

def pie_plot(combatresult, text, xinch=5, yinch=5, res=100):
    # plot Pie chart, where the slices will be ordered and plotted counter-clockwise:
    wins = combatresult[0]
    draws = combatresult[1]
    losses = combatresult[2]
    numbers = [wins, draws, losses]
    labels = f'win:\n{wins}', f'draw:\n{draws}', f'loose:\n{losses}'
    explode = (0.1, 0.0, 0.0)  # only "explode" the 1st (wins) slice
    fi, ax1 = plt.subplots(figsize=(xinch, yinch), dpi=res)  # inch x inch, dpi
    ax1.pie(numbers, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True,  startangle=0)
    ax1.set(title=text ) # + " (n={})".format(len(combatresult)))
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig = plt.gcf()
    return fig #plt.show()

def calculate_dicetext():
    """calculates curent dicetext and updates form"""
    try:
        dicetext1 = "{}{}{}{}{} with{} re-rolling".format(
            values["dice1"],
            "D" if values["reroll1"] else "d",
            values["sides1"],
            "+" if int(values["correction1"]) >= 0 else "-",
            abs(int(values["correction1"])),
            "" if values["reroll1"] else "out",
            )
    except:
        dicetext1 = "error"
    #window["string1"].update(dicetext1.split(" ")[0])
    try:
        dicetext2 = "{}{}{}{}{} with{} re-rolling".format(
            values["dice2"],
            "D" if values["reroll2"] else "d",
            values["sides2"],
            "+" if int(values["correction2"]) >= 0 else "-",
            abs(int(values["correction2"])),
            "" if values["reroll2"] else "out",
            )
    except:
        dicetext2 = "error"
    #window["string2"].update(dicetext2.split(" ")[0])
    return dicetext1, dicetext2


def update_dicestring():
    """calculate the dicestrings from the formular fields"""
    dicetext1, dicetext2 = calculate_dicetext()
    window["string1"].update(dicetext1.split(" ")[0])
    window["string2"].update(dicetext2.split(" ")[0])

# --- helper code to include matplotlib---
def draw_figure(canvas, figure):
    if canvas.children:  # otherwise, the canvas grows bigger each time
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def export():
    # export combattext as csv
    filename = sg.PopupGetFile("enter an csv filename to overwrite or click on 'Browse' to select/create a file",
                               title="choose file to save",
                               default_extension=".csv")
    if filename[-4:] != ".csv":
        sg.Popup("you must create/choose a .csv file! Export canceled")
        return
    with open(filename, "w") as f:
        f.write(str(("round", "Player A", "Player B", "difference", "winner")).strip("()") + "\n")
        for line in window["combatlog"].Values:
            f.write(str(line).strip("[]") + "\n")
    sg.Popup("csv file sucessfully created!")


def swap():
    """swap the values of Player A with those of Player B
    does NOT make a new calculation, only changes the content of form fields"""
    update_dicestring()
    a = [values["dice1"], values["sides1"], values["reroll1"], values["correction1"]]
    b = [values["dice2"], values["sides2"], values["reroll2"], values["correction2"]]
    window["dice1"].update(b[0])
    window["dice2"].update(a[0])
    window["sides1"].update(b[1])
    window["sides2"].update(a[1])
    window["reroll1"].update(b[2])
    window["reroll2"].update(a[2])
    window["correction1"].update(b[3])
    window["correction2"].update(a[3])
    # swapped update of dicestring values!
    dicetext1, dicetext2 = calculate_dicetext()
    window["string1"].update(dicetext2.split(" ")[0])
    window["string2"].update(dicetext1.split(" ")[0])


def make_plots():
    # update matplotlib plots
    result1 = calculate(int(values["howmuch"]), int(values["dice1"]),
                        int(values["sides1"]), values["reroll1"], int(values["correction1"]))
    result2 = calculate(int(values["howmuch"]), int(values["dice2"]),
                        int(values["sides2"]), values["reroll2"], int(values["correction2"]))
    # print("result:", result)
    dicetext1, dicetext2 = calculate_dicetext()
    window["string1"].update(dicetext1.split(" ")[0])
    window["string2"].update(dicetext2.split(" ")[0])
    # plotting...
    # combat result A vs B
    combatresult = []
    combattext = []

    for i in range(len(result1)):
        sg.OneLineProgressMeter("calculating results, please wait",
                                i,
                                len(result1) - 1,
                                key="meter1",
                                orientation="h",
                                )
        combatresult.append(result1[i] - result2[i])
        combattext.append([i + 1, int(result1[i]), int(result2[i]), int(combatresult[i]),
                           "=" if result1[i] == result2[i] else
                           "A" if result1[i] > result2[i] else "B"])
    sg.OneLineProgressMeterCancel(key="meter1")

    window["combatlog"].update(combattext)

    fig = draw_plot(result1, "A: " + dicetext1, 4, 4, 100, None)  # inch x inch, dpi
    fig_canvas_agg = draw_figure(window['CANVAS1'].TKCanvas, fig)
    fig2 = draw_plot(result2, "B: " + dicetext2, 4, 4, 100, None)
    fig_canvas_agg = draw_figure(window["CANVAS2"].TKCanvas, fig2)

    text = "A:" + dicetext1.split(" ")[0] + " vs. B: " + dicetext2.split(" ")[0]
    fig3 = draw_plot(combatresult, text, 12.2, 4, 100, True, combatresult)
    fig_canvas_agg = draw_figure(window['CANVAS3'].TKCanvas, fig3)
    fig4 = pie_plot(combatresult, text, 4, 4, 100)
    fig_canvas_agg = draw_figure(window['CANVAS4'].TKCanvas, fig4)




def main():
    monsterlist = ["wolf","dwarf","human","elf","orc","giant"]

    guis =[None, None]
    for nr, x in enumerate("AB"):
        guis[nr] = sg.Column(layout=[
            [sg.Text("Player"+x), sg.Combo(monsterlist, size=(15, 1), key="template"+x)],
            [sg.Text("name:", size=(10, 1), ), sg.InputText("monster"+x, key="name"+x, size=(15, 1))],
            [sg.Text("HP:", size=(10, 1), ), sg.InputText("10", key="hp"+x, size=(7, 1))],
            [sg.Text("attack", size=(10, 1)), sg.InputText("2D6+0", key="attack"+x, size=(7, 1))],
            [sg.Text("defense", size=(10, 1)), sg.InputText("2D6+0", key="defense"+x, size=(7, 1))],
            [sg.Text("damage", size=(10, 1)), sg.InputText("2d4+1", key="damage"+x, size=(7, 1))],
            [sg.Text("protection", size=(10, 1)), sg.InputText("1D6+0", key="protection"+x, size=(7, 1))],
            [sg.Checkbox("heal after fight", True, key="heal"+x)],
        ])

    #[sg.Canvas(key="CANVAS1")],
    #[sg.Canvas(key="CANVAS2")],
    diagrams = sg.Column(layout=[
        [sg.Canvas(key="CANVAS4"),
         sg.Canvas(key="CANVAS1"),
         sg.Canvas(key="CANVAS2")],
        [sg.Canvas(key="CANVAS3")],

   ])

    forms = sg.Column(layout = [
                [guis[0], guis[1]],
                [sg.Text("# of fights:"), sg.InputText("20", key="number_of_fights", size=(5,1)),
                 sg.Text("max. rounds pro fight:"), sg.InputText("5", key="maxrounds", size=(5,1)),
                 sg.Button("Fight"),  sg.Cancel()],
             ])

    layout = [
                [diagrams],
                [forms, sg.Output(size=(90, 16), font=("CourierNew", 10))  ]
              ]


#  sg.Output(size=(90, 16), font=("CourierNew", 10))

    window = sg.Window('Have some Matplotlib....', layout, finalize=True, element_justification='center')

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        if event == "Fight":
            wins, draws, losses = 0, 0, 0
            end_hp_a = []  # hp at end of each fight
            end_hp_b = []
            dataA = [] # hp at end of each round
            dataB = []
            playerA = Player(values["nameA"], values["hpA"], values["attackA"], values["defenseA"], values["damageA"], values["protectionA"])
            playerB = Player(values["nameB"], values["hpB"], values["attackB"], values["defenseB"], values["damageB"], values["protectionB"])
            ##full_A = playerA.hp
            ##full_B = playerB.hp
            for fnumber in range(int(values["number_of_fights"])):
                sg.OneLineProgressMeter("fighting, please wait",
                                            fnumber,
                                            int(values["number_of_fights"]),
                                            key="meter1",
                                            orientation="h",
                                            )
                print("====== fight # {} ========".format(fnumber))
                if values["healA"]:
                    playerA.heal() # important to restore hp to full after each fight
                elif playerA.hp <= 0:
                    break

                if values["healB"]:
                    playerB.heal()
                elif playerB.hp <=0:
                    break

                dataA.append(playerA.hp)
                dataB.append(playerB.hp)
                ##playerA.hp = full_A
                ##playerB.hp = full_B
                for rnumber in range(int(values["maxrounds"])):
                    print("----- fight # {} round # {}: -----".format(fnumber, rnumber))
                    print(fight(playerA, playerB))
                    dataA.append(playerA.hp)
                    dataB.append(playerB.hp)
                    if playerA.hp <= 0 or playerB.hp <= 0:
                        break
                else:
                    print("***** result: draw *******")
                    draws += 1
                    end_hp_a.append(playerA.hp)
                    end_hp_b.append(playerB.hp)
                    continue # next fight
                if playerA.hp > playerB.hp:
                    print("***** result: A wins")
                    wins += 1
                    end_hp_a.append(playerA.hp)
                    end_hp_b.append(playerB.hp)
                    continue
                else:
                    print("***** result: B wins")
                    losses += 1
                    end_hp_a.append(playerA.hp)
                    end_hp_b.append(playerB.hp)
                    continue
            sg.OneLineProgressMeterCancel(key="meter1")
            print("==========================================")
            print("wins, draws, losses:", wins, draws, losses)
            fig1 = histogram_plot(end_hp_a, "hp of player A after fight", 4, 3, 100)
            fig_canvas_agg = draw_figure(window["CANVAS1"].TKCanvas, fig1)
            fig2 = histogram_plot(end_hp_b, "hp of player B after fight", 4, 3, 100)
            fig_canvas_agg = draw_figure(window["CANVAS2"].TKCanvas, fig2)
            fig4 = pie_plot([wins, draws, losses],
                            "A vs. B:", 4, 3, 100)
            fig_canvas_agg = draw_figure(window['CANVAS4'].TKCanvas, fig4)
            fig3 = line_plot(dataA, dataB, "hp over time", 12.1, 3, 100)
            fig_canvas_agg = draw_figure(window['CANVAS3'].TKCanvas, fig3)


        if event == "export":
            export()



    window.close()

if __name__ == "__main__":
    main()



    ## testing dice_from_string
    #print(dice_from_string("1d6-cf"))
    #dice_from_string("1d6+1")
    #dice_from_string("1d6-2")
    #dice_from_string(" 1d6")
    #dice_from_string("15d6 ")
    #dice_from_string(" 1d6 ")
    #dice_from_string("3D6+1")
    #dice_from_string("20D12+22")
    ## testing dicethrow
    #for i in range(20):
    #    print(dicethrow(*dice_from_string("1d6+0")[0]))
