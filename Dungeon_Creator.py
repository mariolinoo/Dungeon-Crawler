import random
import os
import sys
import PySimpleGUI as sg

# Drunk Walk startet nicht immer in der Mitte des Feldes (Mitte des Feldes ist manchmal verbaut)
""" Erstellt automatisch Dungeons"""


def check_files():
    """Scannt für .dungeon files und liefert die höchste freie Indexnummer"""
    max_i = 0
    for root, dirs, files in os.walk(
            '.'):  # '.' weil aktuelles Verzeichnis, root und dirs sind platzhalter für die rückgabewerte
        for file in files:
            if file.endswith(".dungeon"):
                pos = file.find(".")
                leftpart = file[:pos]
                if leftpart.isdecimal():
                    # print(leftpart,leftpart.isdecimal())
                    if int(leftpart) > max_i:
                        max_i = int(leftpart)
        # print (f"I found the index {max_i}")
        return max_i + 1


def dungeon_base(max_x, max_y):
    dungeon = [["#" for x in range(max_x)] for y in range(max_y)]
    for x in range(max_x):
        for y in range(max_y):
            if y == 0 or y == (max_y - 1):
                dungeon[y][x] = "\u2550"  # ═ ; Erste und letzte Zeile
            elif x == 0 or x == (max_x - 1):
                dungeon[y][x] = "\u2551"  # ║  ; Erste und letzte Spalte
    dungeon[0][0] = "\u2554"  # Topleft
    dungeon[0][max_x - 1] = "\u2557"  # Topright
    dungeon[max_y - 1][0] = "\u255A"  # Bottomleft
    dungeon[max_y - 1][max_x - 1] = "\u255D"  # Bottomright

    return dungeon


def check_infill(dungeon):
    walls = 0
    ground = 0
    # flatten list (dungeon is a list of lists)
    flat_dungeon = [char for row in dungeon for char in row]
    ground = flat_dungeon.count(".")
    field = len(dungeon) * len(dungeon[0])
    return ground / field


def main(number_of_levels=1, target_dir="dungeon_maps", max_x=100, max_y=100, min_infill=0.5, max_infill=0.5,
         verbose=False):
    # TO DO
    # Sysargumente übernehmen und überprüfen
    # Ordnerkreierung gründlicher überprüfen

    steps = 15000
    try:
        os.chdir(target_dir)  # Führt einen cd befehl aus um in das Target direcotry zu gehen
    except FileNotFoundError:
        os.mkdir(target_dir)
        os.chdir(target_dir)

    i = check_files()
    question_txt = f"Number of leves: {number_of_levels}\n Max x: {max_x}\n Max y: {max_y}\n Min and max infill (Walls/Ground ratio): {min_infill * 100}% {max_infill * 100}%\n Verbose : {verbose}\n\n Do you accept this?"
    command = sg.popup_yes_no(question_txt, title="Parameter")
    # print (command)
    pos = [max_y // 2, max_x // 2]  # mid point of the dungeon  # //2 teilt es in zwei und erstellt einene Integer
    if command == "No":
        # Hauptmenü
        layout = [
            [sg.Text("Parameter:", size=(15, 1))],
            [sg.Text("Number of Levels:", size=(15, 1)),
             sg.Input(key='number', size=(15, 1), default_text=str(number_of_levels))],
            [sg.Text("Minimal infill: ", size=(15, 1)),
             sg.Slider([0.3, 0.7], orientation="h", default_value=min_infill, resolution=0.01, size=(15, 15),
                       key="s_min_infill")],
            [sg.Text("Maximal infill: ", size=(15, 1)),
             sg.Slider([0.3, 0.7], orientation="h", default_value=max_infill, resolution=0.01, size=(15, 15),
                       key="s_max_infill")],
            [sg.Text("Max x:", size=(15, 1)), sg.Input(key='max_x', size=(15, 1), default_text=str(max_x))],
            [sg.Text("Max y:", size=(15, 1)), sg.Input(key='max_y', size=(15, 1), default_text=str(max_y))],
            [sg.Button("Confirm", size=(15, 1), key="confirm")],
        ]
        window = sg.Window('Parameter', layout)
        event, values = window.read()
        # print (values)
        if event == "confirm":
            number_of_levels = int(values["number"])
            max_x = int(values["max_x"])
            max_y = int(values["max_y"])
            min_infill = float(values["s_min_infill"])
            max_infill = float(values["s_max_infill"])
        window.close()

    # Progress Window
    layout = [[sg.Text('Progress bar for dungeon creation')],
              [sg.Text('Dungeonlevels')],
              [sg.ProgressBar(number_of_levels, orientation='h', size=(20, 20), key='progressbar1')],
              [sg.Text('Individual dungeon creation')],
              [sg.ProgressBar(steps, orientation='h', size=(20, 20), key='progressbar2')],
              [sg.Output(size=(30, 5))],
              ]

    window = sg.Window('Custom Progress Meter', layout)
    progress_bar1 = window['progressbar1']
    progress_bar2 = window['progressbar2']

    # i ist die höchste gefundene fileindexnummer
    for j in range(i, i + number_of_levels):
        # Init the dungeon parameters for each turn
        dungeon = dungeon_base(max_x, max_y)  # dungeon structure
        infill_perc = random.uniform(min_infill,
                                     max_infill)  # Creates a random infill-recentage between min and max for each dungeon

        for step in range(steps):
            dy, dx = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            y, x = pos[0], pos[1]
            # Läuft in eine Grenze und wird auf die andere Setie befördert
            if x + dx == 0:
                dx = max_x - 2 - x
            elif y + dy == 0:
                dy = max_y - 2 - y
            elif x + dx == (max_x - 1):
                dx = -x + 1
            elif y + dy == (max_y - 1):
                dy = -y + 1
            pos = [y + dy, x + dx]
            y, x = pos[0], pos[1]
            # Create Way
            dungeon[y][x] = "."
            dung_infill = check_infill(dungeon)
            if dung_infill > infill_perc:
                break
            if (step % 100 == 0):
                event, values = window.read(timeout=1e-10)
                progress_bar1.UpdateBar(j - i)
                progress_bar2.UpdateBar(step + 1)

        else:
            # For-Schleife lief 15k mal durch ohne einen Break
            UserWarning(f"Dungeon {j} used 15k steps without a break")

        if verbose:
            for line in dungeon:
                print("".join(line))  # verbindet die lines mit "" einander

        # Test der Mitte
        # dungeon[max_y // 2][max_x // 2]="O"
        with open(str(j) + ".dungeon", "w") as f:
            for line in dungeon:
                f.write("".join(line))
                f.write("\n")
        print(f'{str(j) + ".dungeon"} ready')

    window.close()
    print("Dungeon creation finished")


if __name__ == "__main__":  # Das Programm wird direkt aufgerufen und nicht durch ein zweites Pythonprogramm gestartet
    if len(sys.argv) > 1:
        main(int(sys.argv[1:]))

    else:
        main()
