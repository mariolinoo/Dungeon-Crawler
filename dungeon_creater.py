import random
import os

#Drunk Walk startet nicht immer in der Mitte des Feldes (Mitte des Feldes ist manchmal verbaut)
"""Erstellt automatisch Dungeons"""

def check_files():
    """Scannt für .dungeon files und liefert die nächste frei Indexnummer"""
    max_i=0
    for root, dirs, files in os.walk('.'): #'.' weil aktuelles Verzeichnis, root und dirs sind platzhalter für die rückgabewerte
        for file in files:
            if file.endswith(".dungeon"):
                pos=file.find(".")
                leftpart=file[:pos]
                if leftpart.isdecimal():
                    if int(leftpart.isdecimal())>max_i:
                        max_i=int(leftpart.isdecimal())
        return max_i+1

def dungeon_base(max_x, max_y):
    dungeon= [["#" for x in range(max_x)] for y in range(max_y)]
    for x in range(max_x):
        for y in range(max_y):
            if y == 0 or y == (max_y-1):
                dungeon[y][x]="\u2550" # ═ ; Erste und letzte Zeile
            elif x == 0 or x == (max_x-1):
                dungeon[y][x] = "\u2551"  # ║  ; Erste und letzte Spalte
    dungeon[0][0] = "\u2554" #Topleft
    dungeon[0][max_x-1] = "\u2557" #Topright
    dungeon[max_y-1][0] = "\u255A" #Bottomleft
    dungeon[max_y-1][max_x-1] = "\u255D" #Bottomright

    return dungeon


def main(max_x=30, max_y=15, infill=0.5, autosave = False, verbose = False):
    i = check_files()
    steps=((max_x*max_y)-(max_x*2+max_y*2))  
    pos=[max_y//2,max_x//2] #//2 teilt es in zwei und erstellt einene Integer
    dungeon = dungeon_base(max_x, max_y)
    while True:
        for step in range(steps):
            dy,dx=random.choice([(0,1),(1,0),(0,-1),(-1,0)])
            y,x=pos[0],pos[1]
            #Läuft in eine Grenze und wird auf die andere Setie befördert
            if x+dx == 0:            
                dx=max_x-2-x
            elif y+dy == 0:
                dy=max_y-2-y
            elif x+dx == (max_x-1):
                dx=-x+1
            elif y+dy == (max_y-1):
                dy=-y+1
            pos=[y+dy, x+dx]
            y,x=pos[0],pos[1]
            #Create Way
            dungeon[y][x]="."
        if verbose:   
            for line in dungeon:
                print("".join(line)) #verbindet die lines mit "" einander
        
        if not autosave:
            command=input("Save with y or q for quit:")
            if command == "q":
                break
        if autosave or command == "y":
            #Test der Mitte
            #dungeon[max_y // 2][max_x // 2]="O"
            with open(str(i) +".dungeon", "w") as f:
                for line in dungeon:
                    f.write("".join(line))
                    f.write("\n")
            print(f'{str(i) + ".dungeon"} ready')
            i+=1
            if autosave:
                break
        else:
            print("Dungeon deleted")
           
    print("Dungeon creation finished")
               
if __name__=="__main__":
    main()
            