import os
from random import randrange
import math

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_win_or_draw(player):
    c=BOARD.coords
    if BOARD.available_moves==[]:
        return None
    for i in range(1,10,3):
        if c[i]==c[i+1] and c[i]==c[i+2] and c[i]==player:
            return True
    for i in range(1,4):
        if c[i]==c[i+3] and c[i]==c[i+6] and c[i]==player:
            return True
    if c[1]==c[5] and c[5]==c[9] and c[1]==player:
        return True
    if c[7]==c[5] and c[5]==c[3] and c[7]==player:
        return True
    return False
        
def int_input(cout):
    while True:
        try:
            inp=input(cout)
            return int(inp)
        except:
            print("***Errore, richiesto intero.")

def singleplayer_setup():
    global PLAYER1,PLAYER2
    clearTerminal()
    print("================ TRIS ================")
    print("------------ Singleplayer ------------")
    print(" 1) CPU")
    print(" 2) Utente")
    scelta=int_input(">>>Chi inizia? ")
    while scelta not in [1,2]:
        scelta=int_input(">>>Scelta non valida. Chi inizia? ")
    if scelta==1:
        PLAYER1=AI(True)
        PLAYER2=User(False)
    else:
        PLAYER1=User(True)
        PLAYER2=AI(False)
    startGame()

def multiplayer_setup():
    global PLAYER1,PLAYER2
    clearTerminal()
    print("================ TRIS ================")
    print("------------ Multiplayer -------------")
    PLAYER1=User(True)
    PLAYER2=User(False)
    startGame()

class Board(object):
    coords={}
    available_moves=[]
    def __init__(self):
        self.coords={
            1:" ",2:" ",3:" ",
            4:" ",5:" ",6:" ",
            7:" ",8:" ",9:" "
        }
        self.available_moves=[1,2,3,4,5,6,7,8,9]
    def insertMove(self,player,square):
        if self.coords[square]==" ":
            self.available_moves.remove(square)
            self.coords[square]=player
        else:
            print(square)
            self.view_board()
            print("Fatal error, killing program now")
            exit()
        
    def view_board(self):
        print("                 MAPPA")
        for i in range(1,len(self.coords)+1):
            if i%3==0:
                print(f" {self.coords.get(i)}     {i-2} | {i-1} | {i}")
                if i!=9:
                    print("---+---+---   ---+---+---")
            else:
                print(f" {self.coords[i]} |",end="")
    def clean_board(self):
        self.__init__()

class Player:
    char=""
    opponent=""
    first=True

    def __init__(self,first):
        self.first=first
        self.isFirst()

    def isFirst(self):
        self.char="X" if self.first else "O"
        self.opponent="O" if self.first else "X"

#ereditarietà
class User(Player):
    def __init__(self,first):
        super().__init__(first)

    def makemove(self,moves):
        global TURN,PLAYER1,PLAYER2
        
        scelta=int_input(">>> Inserire mossa (numero quadrato): ")
        while scelta not in moves:
            scelta=int_input(">>> Mossa non valida. Inserire mossa (numero quadrato): ")
        return scelta
#ereditarietà
class AI(Player):
    def __init__(self,first):
        super().__init__(first)
        
    def makemove(self, _ ):
        #self.reset_move()
        #depth=len(BOARD.available_moves)
        #return moves[randrange(len(moves))]
        a=dict(BOARD.coords) #make a copy
        #return 5 if depth==9 else (self.movechoice(a,depth,True,True))[0]
        return self.make_best_move(a)

    def calculate_board_state(self, board): #return W win, L lose, D draw, N not over
        c=dict(board) #copio board
        #combinazioni di vittoria orizzontali
        for i in range(1,10,3):
            if c[i]==c[i+1] and c[i]==c[i+2] and c[i]==self.char:
                return "W"
            if c[i]==c[i+1] and c[i]==c[i+2] and c[i]==self.opponent:
                return "L"
        #combinazioni di vittoria verticali
        for i in range(1,4):
            if c[i]==c[i+3] and c[i]==c[i+6] and c[i]==self.char:
                return "W"
            if c[i]==c[i+3] and c[i]==c[i+6] and c[i]==self.opponent:
                return "L"
        #combinazioni di vittoria diagonali
        if c[1]==c[5] and c[5]==c[9] and c[1]==self.char:
            return "W"
        if c[1]==c[5] and c[5]==c[9] and c[1]!=self.char:
            return "L"
        if c[7]==c[5] and c[5]==c[3] and c[7]==self.char:
            return "W"
        if c[7]==c[5] and c[5]==c[3] and c[7]!=self.char:
            return "L"
        #controllo pareggio
        for key in c:
            if c[key] == " ":
                return "N"
        return "D"

    def make_best_move(self,board):
        bestScore = - math.inf
        bestMove = None
        for move in board:
            if board[move] == " ":
                board[move] = self.char
                a=dict(board)
                score = self.minimax(False, a)
                board[move] = " "
                if score > bestScore:
                    bestScore = score
                    bestMove = move
        return bestMove

    def minimax(self, myTurn, board):
        match self.calculate_board_state(board):
            case "D":
                return 0
            case "W":
                return +1
            case "L":
                return -1
        scores=[]
        for move in board:
            if board[move]==" ":
                board[move]=self.char if myTurn else self.opponent
                a=dict(board)
                scores.append(self.minimax(not myTurn, a))
                board[move]=" "
        return max(scores) if myTurn else min(scores)

gamemodes={
    1:singleplayer_setup,
    2:multiplayer_setup
}
PLAYER1=None
PLAYER2=None
BOARD=Board()
TURN=True #true for player1, false for player2

def menu():
    clearTerminal()
    print("================ TRIS ================")
    print(" 1) Singleplayer")
    print(" 2) Multiplayer\n")
    scelta=int_input(">>> Inserire modalità di gioco: ")
    while scelta not in [1,2]:
        scelta=int_input(">>> Scelta non valida. Inserire modalità di gioco: ")
    gamemodes[scelta]()
        

def startGame():
    global PLAYER1,PLAYER2,TURN
    player=PLAYER1.char
    while check_win_or_draw(player)!=True and check_win_or_draw(player) is not None:
        player=PLAYER1.char if TURN else PLAYER2.char
        moves=BOARD.available_moves
        clearTerminal()
        print("================ TRIS ================")
        print(f"\n*** TURNO DI {player} ***")
        BOARD.view_board()
        if TURN:   
            square=PLAYER1.makemove(moves)
            char=PLAYER1.char
        else:
            square=PLAYER2.makemove(moves)
            char=PLAYER2.char
        TURN=not TURN
        BOARD.insertMove(char,square)
    clearTerminal()
    print("================ TRIS ================")
    BOARD.view_board()
    match check_win_or_draw(PLAYER1.char):
        case True:
            print(f"*** {PLAYER1.char} VINCE! ***")
        case False:
            print(f"*** {PLAYER2.char} VINCE! ***")
        case _:
            print("*** PAREGGIO! ***")
    BOARD.clean_board()

def main():
    menu()
    
main()