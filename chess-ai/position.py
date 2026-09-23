#formato posizione
#k re, n cavallo, r torre, q regina, p pedone, b alfiere, / riga succ, bianco maiusc nero min,

starting_pos="rnbkqbnr8p32 8PRNBKQBNR-w"
white_turn=False

board={
    0:"",1:"",2:"",3:"",4:"",5:"",6:"",7:"",
    8:"",9:"",10:"",11:"",12:"",13:"",14:"",15:"",
    16:"",17:"",18:"",19:"",20:"",21:"",22:"",23:"",
    24:"",25:"",26:"",27:"",28:"",29:"",30:"",31:"",
    32:"",33:"",34:"",35:"",36:"",37:"",38:"",39:"",
    40:"",41:"",42:"",43:"",44:"",45:"",46:"",47:"",
    48:"",49:"",50:"",51:"",52:"",53:"",54:"",55:"",
    56:"",57:"",58:"",59:"",60:"",61:"",62:"",63:""
}

def insert_position(position):
    global white_turn
    pos,turn=position.split("-")
    index=0 #indice dizionario
    for i in range(len(pos)):
        if index==64:
            break
        piece=pos[i]
        if piece.isdigit() and pos[i:i+2].isdigit():
            
            p=pos[i+2] #dato da inserire int(pos[i:i+2]) volte nel dizionario

            for k in range(int(pos[i:i+2])):
                board[index]=p
                index+=1
            pos=pos[:i+1]+pos[i+3:] #salto i 2 caratteri successivi

        elif piece.isdigit():
            p=pos[i+1]
            for k in range(int(piece)):
                board[index]=p
                index+=1
            pos=pos[:i+1]+pos[i+2:] #salto il carattere successivo
        else:
            board[index]=piece
            index+=1
    white_turn=(str(turn)=="w") 

"""
    mosse
    ALFIERE: 
    -9  -7
    +7  +9
    TORRE:
    +8 -8 +1 -1
    CAVALLO:
    -17  -15
    -10  -6
    +6   +10
    +15  +17
    PEDONE:
    +8,-8,+16,-16, cattura +7, +9, -9, -7
"""