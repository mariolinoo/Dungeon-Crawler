import os
import os.path
import PySimpleGUI as sg
import glob
import name_fill

class GUI:
    window = None
    screen_dim = (1880, 1000)


def scan_folder(path_to_folder):
    max_x=0
    max_y=0
    max_filename=0

    files = glob.glob(os.path.join(path_to_folder, "*.dungeon"))
    files.sort()
    file_names = [f[len(path_to_folder) + 1:] for f in files]
    file_num = len(file_names)

    for file in file_names:
        max_filename = max(max_filename, len(file))
        with open(os.path.join(path_to_folder, file)) as f:
            lines = f.readlines()
            y = len(lines)
            x = len(lines[0].strip())
            max_x = max(x, max_x)
            max_y = max(y, max_y)

    return max_filename, max_x, max_y, file_num


def main():
    #ToDo Scrollable anzeige damit sich beliebige Dungeonanzahl ausgeht
    #Abfrage nach dem Zielordner
    path_to_folder = None
    while path_to_folder is None:
        path_to_folder = sg.popup_get_folder("Please select folder for preview")
        if path_to_folder is None or path_to_folder == "":
            if sg.popup_yes_no("Do you want to cancel?") == "Yes":
                return

    #füllt die indexnummer mit 0er auf, damit die sortfunktion funktioniert
    name_fill.main(path_to_folder)

    #Überprüfen des Ordnerinhalts
    max_filename, max_x, max_y, file_num = scan_folder(path_to_folder)
    print(max_filename, max_x, max_y, file_num)

    left = sg.Column([[sg.Text(str(i)+": ")] for i in range(0,file_num, 10)])
    layout  =   [
                    [sg.Text(), sg.Text("0 1 2 3 4 5 6 7 8 9")],
                    [left, sg.Graph(background_color="#FFFFFF", canvas_size= GUI.screen_dim, graph_bottom_left= (0,GUI.screen_dim[1]),graph_top_right=(GUI.screen_dim[0], 0), key="canvas")]
                ]

    GUI.window = sg.Window('Folderbrowser', layout)


    event, values = GUI.window.read()




if __name__ == "__main__":
    main()