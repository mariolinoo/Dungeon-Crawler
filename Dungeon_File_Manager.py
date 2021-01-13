import os
import os.path
import PySimpleGUI as sg
import glob
import shutil
import name_fill

class GUI:
    window = None
    default = "Please select Folder"
    button_size = (7, 2)

def update_file_list(folder_path_old, folder_path_new):
    for path in (folder_path_new, folder_path_old):
        if path is None or path == "":
            continue
        # File wird gelöscht und die Listbox muss neu geladen werden
        files = glob.glob(os.path.join(path, "*.dungeon"))
        files.sort()
        # print(files)
        file_names = [f[len(path) + 1:] for f in files]
        if path == folder_path_old:
            GUI.window["content"].Update(values=file_names)
        elif path == folder_path_new:
            GUI.window["new_content"].Update(values=file_names)

def move_file(old_path, new_path):
    # File sol bewegt werden und die Listbox muss neu geladen werden
    try:
        shutil.move(old_path, new_path)
    except:
        sg.PopupOK("Move action failed")

def content_display(folder, content, left):
    if content != GUI.default:
        print(f"you selected {content}")
        name = os.path.join(folder, content)
        # print(name)
        with open(name) as dungeon_file:
            text = dungeon_file.readlines()
        # dungeon_preview = "".join(text)
        if left:
            c = GUI.window["canvas_left"]
        else:
            c = GUI.window["canvas_right"]
        c.DrawRectangle((0, 0), (100, 100), line_color='white', fill_color='white')

        for y, line in enumerate(text):
            for x, char in enumerate(line):
                if char == "#":
                    c.DrawRectangle((x, y), (x + 1, y + 1), line_color='black', fill_color='black')
                elif char == ".":
                    pass
                else:
                    # Unicode walls
                    c.DrawRectangle((x, y), (x + 1, y + 1), line_color='purple', fill_color='purple')
                    # dasselbe wie bei #
        # GUI.window["canvas"].Update(dungeon_preview)
        if left:
            GUI.window["Mov"].Update(disabled=False)
            GUI.window["Del"].Update(disabled=False)
            GUI.window["Zerofill"].Update(disabled=False)

        else:
            GUI.window["Mov Back"].Update(disabled=False)
            GUI.window["Del 2"].Update(disabled=False)
            GUI.window["Zerofill 2"].Update(disabled=False)

def delete_file(folder, content):
    name = os.path.join(folder, content)
    os.remove(name)
    # File wird gelöscht und die Listbox muss neu geladen werden

def main():
    #ToDo Filemanager in Duneon einbinden, Folderliste erstellen, Im layout den gewählten Pfad zeigen
    left = sg.Column([
                        [sg.Text('Old Folder: ')],
                        [sg.Input(key="folder", enable_events=True, visible=True, readonly = True)],
                        [sg.FolderBrowse(target="folder", size = GUI.button_size)],
                        [sg.Listbox(values=[GUI.default], enable_events=True, select_mode="LISTBOX_SELECT_MODE_SINGLE",key="content", size=(30, 20))],
                    ])
    middle_left = sg.Column([
                        [sg.Graph(background_color="#FFFFFF", canvas_size=(300, 300), graph_bottom_left=(0, 100), graph_top_right=(100, 0), key="canvas_left")],
                    ])
    middle_right = sg.Column([
                        [sg.Text('New Folder:')],
                        [sg.Input(key="new_folder", enable_events = True, visible=True, readonly = True)],
                        [sg.FolderBrowse(target="new_folder", size=GUI.button_size)],
                        [sg.Listbox(values=[GUI.default], enable_events=True, select_mode="LISTBOX_SELECT_MODE_SINGLE", key="new_content", size=(30, 20))],
                    ])

    right = sg.Column([
                        [sg.Graph(background_color="#FFFFFF", canvas_size=(300, 300), graph_bottom_left=(0, 100),graph_top_right=(100, 0), key="canvas_right")],
                    ])


    layout =[
                [left, middle_left, middle_right, right],
                [sg.Button("Del", disabled =True, size=GUI.button_size), sg.Button("Del 2", disabled =True, size=GUI.button_size), sg.Button("Mov", disabled=True, size=GUI.button_size), sg.Button("Mov Back", disabled=True, size=GUI.button_size), sg.Button("Zerofill", disabled=True, size=GUI.button_size), sg.Button("Zerofill 2", disabled=True, size=GUI.button_size)],
                [sg.Cancel(key="Cancel", size=GUI.button_size), sg.Ok(key="Ok", size=GUI.button_size)],
            ]
    GUI.window = sg.Window('Folderbrowser', layout)
    old_path, new_path = None, None

    while True:
        #Events müssen kontinuirlich ausgelesen werden
        event, values = GUI.window.read()
        GUI.window["Del"].Update(disabled=True)
        GUI.window["Del 2"].Update(disabled=True)
        GUI.window["Mov"].Update(disabled=True)
        GUI.window["Mov Back"].Update(disabled=True)
        GUI.window["Zerofill"].Update(disabled=True)
        GUI.window["Zerofill 2"].Update(disabled=True)

        #Folder ausgewählt
        if event in (sg.WIN_CLOSED, "Cancel"):
            break

        if event == "folder" or event == "new_folder":
            # Files sortieren und auflisten
            update_file_list(values["folder"], values["new_folder"])

        if event == "content":
            content_display(values["folder"], values["content"][0], True)
        if event == "new_content":
            content_display(values["new_folder"], values["new_content"][0], False)

        if event == "Del":
            delete_file(values["folder"], values["content"][0])
            update_file_list(values["folder"], values["new_folder"])
            GUI.window["canvas_left"].DrawRectangle((0, 0), (100, 100), line_color='white', fill_color='white')

        if event == "Del 2":
            delete_file(values["new_folder"], values["new_content"][0])
            update_file_list(values["folder"], values["new_folder"])
            GUI.window["canvas_right"].DrawRectangle((0, 0), (100, 100), line_color='white', fill_color='white')

        if event == "Mov":
            old_path = os.path.join(values["folder"], values["content"][0])
            new_path = os.path.join(values["new_folder"], values["content"][0])
            move_file(old_path, new_path)
            update_file_list(values["folder"], values["new_folder"])
            GUI.window["canvas_left"].DrawRectangle((0, 0), (100, 100), line_color='white', fill_color='white')

        if event == "Mov Back":
            old_path = os.path.join(values["new_folder"], values["new_content"][0])
            new_path = os.path.join(values["folder"], values["new_content"][0])
            move_file(old_path, new_path)
            update_file_list(values["folder"], values["new_folder"])
            GUI.window["canvas_right"].DrawRectangle((0, 0), (100, 100), line_color='white', fill_color='white')

        if event == "Zerofill":
            name_fill.main(values["folder"])
            update_file_list(values["folder"], values["new_folder"])

        if event == "Zerofill 2":
            name_fill.main(values["new_folder"])
            update_file_list(values["folder"], values["new_folder"])

        #Filebrowser fertig
        if event == "Ok":
            myfolder = values["folder"]
            #myfile = values["file"]
            #print("Chosen file", myfile)
            #break

    GUI.window.close()


if __name__ == "__main__":
    main()

