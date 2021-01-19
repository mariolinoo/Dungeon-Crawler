import os
import os.path
import PySimpleGUI as sg
import glob
import name_fill

class GUI:
    window = None
    #Canvas auf dem die kleinen Thumbnails gezeichnet werden
    thumbnail_canvas = [1270, 800] # = [Px]
    #Canvas auf dem eine große Virschau des Dungeons gezeigt wird
    preview_canvas = [500,500] # = [Px]
    #Gr. der Schaltfläche
    button_size = (7, 2) # = [char]
    #Abstand zwischen Thumbnails
    padding_x = 10 # = [Px]
    padding_y = 20 # = [Px]
    #Liste aller Filenames mit ihrem Pfad
    complete_filenames = []
    #Bereinigte Filenames ohne Pfad
    file_names = []
    #Maximale Größe der Dungeons
    max_x = 0 # = [char]
    max_y = 0 # = [char]
    #Anzahl der Dungeons im Ordner
    file_num = 0
    #Längster Name (Für die Anzeige und das sort())
    max_length_filename = 0
    #Maximale Pixelgröße des Thumbnails inklusive Padding
    px_x = 0 # = [Px]
    px_y = 0 # = [Px]
    #Anzahl der maximalen Spalten
    max_cols = 0
    #Benötigte Spalten und Zeilen
    rows = 0
    cols = 0

def scan_folder(path_to_folder):

    files = glob.glob(os.path.join(path_to_folder, "*.dungeon"))
    files.sort()
    GUI.complete_filenames = files
    GUI.file_names = [f[len(path_to_folder) + 1:] for f in files]
    GUI.file_num = len(GUI.file_names)

    for file in GUI.file_names:
        GUI.max_length_filename = max(GUI.max_length_filename, len(file))
        with open(os.path.join(path_to_folder, file)) as f:
            lines = f.readlines()
            y = len(lines)
            x = len(lines[0].strip())
            GUI.max_x = max(x, GUI.max_x)
            GUI.max_y = max(y, GUI.max_y)


def calc_table():
    GUI.max_cols = max(1, int(GUI.thumbnail_canvas[0] / (GUI.max_x + GUI.padding_x)))
    GUI.cols = min(GUI.file_num, GUI.max_cols)
    GUI.px_x = GUI.max_x + GUI.padding_x
    GUI.thumbnail_canvas[0] = (GUI.max_cols * GUI.px_x)

    GUI.rows = max(1, int(GUI.file_num / GUI.cols))
    GUI.px_y = (GUI.max_y+GUI.padding_y)
    GUI.thumbnail_canvas[1] = (GUI.max_y+GUI.padding_y) * GUI.rows


def draw_grid(): #Graph Koordinatensystem Oben links 0,0 unten rechts max_x,max_y y nach unten positiv
    c = GUI.window["thumbnail_canvas"]
    #c.DrawLine((0,0), (500,100), color="black")
    #Verticale Linien
    for x in range(0, (GUI.px_x * GUI.cols)+1 , GUI.px_x): #(von, bis exclusiv, step)
        start = (x, 0)
        end = (x, GUI.thumbnail_canvas[1])
        c.DrawLine(start, end, color = "black")
    print(GUI.thumbnail_canvas[0], GUI.thumbnail_canvas[1])
    #Horizontale Linien
    for y in range(0, (GUI.px_y * GUI.rows)+1, GUI.px_y):
        start = (0, y)
        end = (GUI.thumbnail_canvas[0], y)
        c.DrawLine(start, end, color = "black")

def draw_thumbnail_canvass():
    c = GUI.window["thumbnail_canvas"]
    #for i in range(len(GUI.complete_filenames)):
    print(GUI.complete_filenames[0])
    i = 0
    for y in range(0, GUI.thumbnail_canvas[1]+1, GUI.px_y):
        for x in range(0, GUI.thumbnail_canvas[0]+1, GUI.px_x):

            #Exitbedingung
            if i >= len(GUI.complete_filenames):
                print("Killed the progressbar")
                sg.one_line_progress_meter_cancel(key = "progress")
                return
            print(i)

            #Auslesen des Files
            with open(GUI.complete_filenames[i]) as dungeon_file:
                text = dungeon_file.readlines()
            sg.one_line_progress_meter("Progressbar creating thumbnail_canvas:", i, len(GUI.complete_filenames), orientation = "h", key = "progress")

            #Zeichnen des Thumbnails
            for ty, line in enumerate(text):
                for tx, char in enumerate(line):
                    if char == "#":
                        start = (tx + x + (GUI.padding_x//2), ty + y)
                        end = (tx + x  + (GUI.padding_x//2) + 1, ty + y + 1)
                        c.DrawRectangle( start, end, line_color='black', fill_color='black')
                    elif char == ".":
                        pass
                    else:
                        # Unicode walls
                        start = (tx + x + (GUI.padding_x//2), ty + y)
                        end = (tx + x + (GUI.padding_x//2) + 1, ty + y + 1)
                        c.DrawRectangle(start, end, line_color='purple', fill_color='purple')

            #Schreiben des Filenamens
            c.draw_text(text = GUI.file_names[i], location = (tx+x - GUI.px_x//2, ty + y + GUI.padding_y//2), font = ("arial", 10))

            i+=1

def main():
    #ToDo Abfangen des Cancels bei de Progressbar
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
    scan_folder(path_to_folder)

    #Kalkuliert anhand des Ornderinhalts Parameter für die Preview
    calc_table()


    #left = sg.Column([[sg.Text(str(i)+": ")] for i in range(0,file_num, 10)], lavout,  scrollable= True)
    left = sg.Column    ([
                            [sg.Graph(background_color="#FFFFFF", canvas_size= GUI.thumbnail_canvas, graph_bottom_left= (0,GUI.thumbnail_canvas[1]),graph_top_right=(GUI.thumbnail_canvas[0], 0), enable_events = True, key="thumbnail_canvas")],
                        ],scrollable = True, size = (1300,900), expand_x = True, expand_y = True
                        )

    right = sg.Column   ([
                            [sg.Graph(background_color="#FFFFFF", canvas_size= GUI.preview_canvas, graph_bottom_left= (0,GUI.max_y),graph_top_right=(GUI.max_x, 0), key="preview")],
                            [sg.Button("Hallo", size = GUI.button_size)],
                            [sg.Cancel(size=GUI.button_size)],
                        ], vertical_alignment = "top"
                        )
    layout  =   [   [sg.Text(f"Infos : Files({GUI.file_num}), max_x({GUI.max_x}), max_y({GUI.max_y})"),],
                    [left,right],
                ]

    GUI.window = sg.Window('Folderbrowser', layout)
    GUI.window.finalize()

    draw_grid()
    draw_thumbnail_canvass()

    while True:
        event, values = GUI.window.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        if event == "thumbnail_canvas":
            print("Click")
            print(event)
            print(values["thumbnail_canvas "])

    GUI.window.close()



if __name__ == "__main__":
    main()