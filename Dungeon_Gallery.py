import os
import os.path
import PySimpleGUI as sg
import glob
import name_fill

class GUI:
    window = None
    thumbnail_dim = [1270, 800]
    screen_dim = [1880, 1000]
    button_size = (7, 2)
    padding_x = 10
    padding_y = 20
    complete_filenames = []


def scan_folder(path_to_folder):
    max_x=0
    max_y=0
    max_filename=0

    files = glob.glob(os.path.join(path_to_folder, "*.dungeon"))
    files.sort()
    GUI.complete_filenames = files
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

def calc_table(max_x, max_y, file_num):
    """Berechnet die Formatierung der Tabelle und gibt zurück ein Tuple zurück
    [0] Anzahl Spalten
    [1] Anzahl Reihen
    [2] Grid_dim x in Pixel
    [3] Grid_dim y in Pixel
    """
    cols = int(GUI.thumbnail_dim[0] / (max_x + GUI.padding_x))
    px_x = max_x + GUI.padding_x
    rows = int(file_num / cols)
    px_y = (max_y+GUI.padding_y)
    GUI.thumbnail_dim[1] = (max_y+GUI.padding_y) * rows
    return (cols, rows, px_x, px_y)

def draw_grid(table_dimension):
    c = GUI.window["Thumbnails"]
    px = table_dimension[2]
    py = table_dimension[3]
    for x in range(0, GUI.thumbnail_dim[0], px):
        start = ( x, 0)
        end = ( x, GUI.thumbnail_dim[1])
        c.DrawLine(start, end, color = "black")
    print(GUI.thumbnail_dim[0], GUI.thumbnail_dim[1])
    for y in range(0, GUI.thumbnail_dim[1], py):
        start = ( 0, y)
        end = ( GUI.thumbnail_dim[0], y)
        c.DrawLine(start, end, color = "black")

def draw_thumbnails(table_dimension):
    c = GUI.window["Thumbnails"]
    px = table_dimension[2]
    py = table_dimension[3]
    for i in range(len(GUI.complete_filenames)):
        sg.one_line_progress_meter("Progressbar creating Thumbnails:", i, len(GUI.complete_filenames), orientation = "h")
        for x in range(0, GUI.thumbnail_dim[0], px):
            for y in range(0, GUI.thumbnail_dim[1], py):
                with open(GUI.complete_filenames[i]) as dungeon_file:
                    text = dungeon_file.readlines()
                for ty, line in enumerate(text):
                    for tx, char in enumerate(line):
                        if char == "#":
                            c.DrawRectangle((tx + x, ty + y), (tx + x+ 1, ty + y+ 1), line_color='black', fill_color='black')
                        elif char == ".":
                            pass
                        else:
                            # Unicode walls
                            c.DrawRectangle((tx + x, ty + y), (tx + x + 1, ty + y + 1), line_color='purple', fill_color='purple')



def main():
    #ToDo Fehler im Thumbnailzeichnen beheben (Funktion draw_thumbnail)
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
    table_dimension = calc_table(max_x, max_y, file_num)

    #left = sg.Column([[sg.Text(str(i)+": ")] for i in range(0,file_num, 10)], lavout,  scrollable= True)
    left = sg.Column    ([
                            [sg.Graph(background_color="#FFFFFF", canvas_size= GUI.thumbnail_dim, graph_bottom_left= (0,GUI.thumbnail_dim[1]),graph_top_right=(GUI.thumbnail_dim[0], 0), key="Thumbnails")],
                        ],scrollable = True, size = (1300,900), expand_x = True, expand_y = True
                        )

    right = sg.Column   ([
                            [sg.Graph(background_color="#FFFFFF", canvas_size= (500,500), graph_bottom_left= (0,GUI.screen_dim[1]),graph_top_right=(GUI.screen_dim[0], 0), key="Preview")],
                            [sg.Button("Hallo", size = GUI.button_size)],
                        ], vertical_alignment = "top"
                        )
    layout  =   [   [sg.Text(f"Infos : Files({file_num}), max_x({max_x}), max_y({max_y})"),],
                    [left,right],
                ]

    GUI.window = sg.Window('Folderbrowser', layout)
    GUI.window.finalize()
    draw_grid(table_dimension)
    draw_thumbnails(table_dimension)
    event, values = GUI.window.read()




if __name__ == "__main__":
    main()