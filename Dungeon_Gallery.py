import os
import os.path
import sys
import PySimpleGUI as sg
import glob



def main():
    #ToDo Filemanager in Duneon einbinden, Folderliste erstellen, Im layout den gewählten Pfad zeigen
    default = "Please select Folder"
    button_size = (7,2)
    left = sg.Column([
                        [sg.Text('Select Folder: ')],
                        [sg.Input(key="folder", enable_events=True, visible=False)],
                        [sg.FolderBrowse(target="folder", size = button_size)],
                        [sg.Listbox(values=[default], enable_events=True, select_mode="LISTBOX_SELECT_MODE_SINGLE",
                                    key="content", size=(30, 20))],
                        # [sg.Input(key="file")],
                        # [sg.FileBrowse(target="file")],
                        [sg.Button("Del", disabled =True, size=button_size), sg.Button("Mov", disabled=True, size=button_size)],
                        [sg.Cancel(key="Cancel", size=button_size), sg.Ok(key="Ok", size=button_size)],
                     ])
    layout =[
                #[left,sg.Multiline(size = (100,100), key = "output", autoscroll = True, font = ("Mono", 6))],
                [left, sg.Graph(background_color = "#FFFFFF", canvas_size = (300, 300), graph_bottom_left=(0,100), graph_top_right=(100,0), key = "canvas")]
            ]
    window = sg.Window('Folderbrowser', layout)


    while True:
        #Events müssen kontinuirlich ausgelesen werden
        event, values = window.read()
        window["Del"].Update(disabled=True)
        window["Mov"].Update(disabled=True)
        #Folder ausgewählt
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event == "folder":
            print("Folderevent")
            # Files auflisten
            files = glob.glob(os.path.join(values["folder"],"*.dungeon"))
            files.sort()
            #print(files)
            file_names = [f[len(values["folder"])+1:] for f in files ]
            window["content"].Update(values = file_names)

        if event == "content":
            if values["content"][0] != default:
                print(f"you selected {values['content']}")
                name= os.path.join(values["folder"],values["content"][0])
                #print(name)
                with open(name) as dungeon_file:
                    text= dungeon_file.readlines()
                #dungeon_preview = "".join(text)
                c=window["canvas"]
                c.DrawRectangle((0, 0), (100, 100), line_color='white', fill_color='white')

                for y,line in enumerate(text):
                    for x, char in enumerate(line):
                        if char == "#":
                            c.DrawRectangle((x, y), (x+1, y+1), line_color='black', fill_color='black')
                        elif char == ".":
                            pass
                        else:
                            pass
                            # dasselbe wie bei #

                #window["canvas"].Update(dungeon_preview)
                window["Del"].Update(disabled = False)
                window["Mov"].Update(disabled = False)

        #Filebrowser fertig
        if event == "Ok":
            myfolder = values["folder"]
            #myfile = values["file"]
            #print("Chosen file", myfile)
            #break


            
    print("Chosen path", myfolder)
    window.close()


if __name__ == "__main__":
    main()

