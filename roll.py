import random

dicelut={
    "1":"\u2680",
    "2":"\u2681",
    "3":"\u2682",
    "4":"\u2683",
    "5":"\u2684",
    "6":"\u2685",}

def wurfel(dicestr="1d6", verbose=True, pretty=True):
    """ Gibt Anzahl der Würfel und Seiten an; D == Reroll d == kein Reroll
        Verbose gibt Würfe aus
        Pretty gibt die Würfe mit Würfeln aus, wenn Würfel < 7
        Delta wird mit dem Dicestr initiert, bei xdy+delta. Delta wird zum Resultat dazugerechnet
        1d3+1 -> resultat +1
        2d4-11 -> resutat -11
    """
    #if "d" not in dice:
    if dicestr.lower().count("d") != 1: #lower() verkleinert alle chars im string (upper() Gegenteil)
        raise ValueError ("Dice must have one d in String")
    pos=dicestr.lower().find("d")
    reroll = False
    if dicestr[pos] == "D":
        reroll = True
    leftpart=dicestr[:pos]
    rightpart=dicestr[pos+1:]
    delta = 0
    pos=rightpart.find("+")
    minus = False
    if pos == -1:
        pos=rightpart.find("-")
        minus = True
    if pos != -1:
        add=rightpart[pos+1:]
        if not add.isdecimal():
            raise ValueError("Strange Dice String")
        if minus:
            delta = -int(add)            
        else:
            delta = int(add)
        rightpart = rightpart[:pos]
    if not leftpart.isdecimal() or not rightpart.isdecimal():
        raise ValueError ("Dice must have numbers and a d splitting them")
    sides=int(rightpart)
    dice=int(leftpart)
    total = 0
    looplist=list(range(dice))
    result =f"{dicestr}: "
    counter=0
    for d in looplist: #kann mit einer WhileSchleife auch erreicht werden
        counter+=1
        roll=random.randint(1,sides)
        total+=roll
        rollstr=str(roll)
        if roll==sides and reroll:
            looplist.append(1)
            total-=1 #-1 damit die höchste zahl gewürfelt werden kann (max + zweiter Wurf kann nicht 0 sein, damit kann max nicht errreicht werden) 
            rollstr=f"{roll}-1"
        result+=rollstr + ("+" if counter != len(looplist) else f"={total}") #Inline If-Abfrage ab dem Operator
    if verbose:
        if pretty and sides < 7:
            resultpretty = ""
            calc=False
            for char in result:
                if char == "=":
                    calc = False
                if char == ":":
                    calc=True
                if char.isdecimal() and calc:
                    resultpretty+=dicelut[char]
                else:
                    resultpretty+=char
            result = resultpretty
    if delta!=0:
        result+=("+" if not minus else "") + str(delta) + f" = {total+delta}"
        
    return total+delta, result

if __name__=="__main__":
    for _ in range(10):
        zahl, string= wurfel("3d6+2")
        print(f"{string}")
    for _ in range(10):   
        zahl, string= wurfel("3D6+2")
        print(f"{string}")
    
