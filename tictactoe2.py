import os
from random import randrange


#pulisce il terminale dagli output precedenti
def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

#gestione errore input non valido sugli interi, il parametro viene stampato
def int_input(cout):
    while True:
        try:
            #prova la conversione, se non ci sono errori ritorno il valore intero
            inp=input(cout) #stampa di cout, contenente stringa per l'input
            return int(inp)
        except:
            #stampo errore, si resta dento al while True e viene chiesto nuovamente l'intero
            print("***Errore, richiesto intero.")

#definita board come classe
class Board(object):
    board=[]
    def __init__(self):
        self.board=[
            [0,0,0],
            [0,0,0],
            [0,0,0]
            ] #la scacchiera viene definita come matrice
        
    #metodo col quale viene aggiornata la board una volta ottenuta la mossa
    def insertMove(self,player,x,y):
        if self.board[x][y]!=0:
            self.board[x][y]=player

    #stampa della board    
    def view_board(self):
        print("                 MAPPA")
        for i in range(len(self.board)):
            if (i+1)%3==0:
                print(" "+(self.board[i] if self.board[i]!=0 else " ") + f"     {i-1} | {i} | {i+1}")
                if i!=8:
                    print("---+---+---   ---+---+---")
            else:
                print(" "+(self.board[i] if self.board[i]!=0 else " ") +" |",end="")
    
    #svuotamento board (viene reinizializzata)
    def clean_board(self):
        self.__init__()

#classe base da cui poi verranno definiti User ed AI
class Player:
    char=""
    opponent=""
    first=True

    def __init__(self,first):
        self.first=first
        self.isFirst()

    #partono le X, gli O vanno secondi
    def isFirst(self):
        self.char="X" if self.first else "O"
        self.opponent="O" if self.first else "X"

#ereditarietà
class User(Player):
    def __init__(self,first):
        super().__init__(first)

    #a ogni indice della matrice corrisponderà un numero che il giocatore potrà scegliere per effettuare la sua mossa
    def makemove(self,moves):
        global TURN,PLAYER1,PLAYER2
        
        scelta=int_input(">>> Inserire mossa (numero quadrato): ") #NB a ogni input di interi verrà SEMPRE usato int_input per gestire l'errore invece di int(input())
        while scelta not in moves:
            scelta=int_input(">>> Mossa non valida. Inserire mossa (numero quadrato): ")
        return scelta

#ereditarietà parte 2
class AI(Player):
    def __init__(self,first):
        super().__init__(first)
        
    def makemove(self,moves):
        #depth=len(BOARD.available_moves) non necessario per tris, necessario per gli scacchi
        return moves[randrange(len(moves))]

#modalità singleplayer, parte player1 e secondo player2, necessario definire chi sarà l'utente e chi l'ai
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
    #assegnazione alle variabili globali, true e false per stabilire chi parte dei 2 e quindi chi deve esssere X e chi O
    if scelta==1:
        PLAYER1=AI(True)
        PLAYER2=User(False)
    else:
        PLAYER1=User(True)
        PLAYER2=AI(False)
    #startGame()

#multiplayer, player1 e player2 verranno entrambi definiti come istanze di User, in questo caso è irrilevante chi inizia in quanto sono entrambi
#istanze di User e X parte sempre per prima
def multiplayer_setup():
    global PLAYER1,PLAYER2
    clearTerminal()
    print("================ TRIS ================")
    print("------------ Multiplayer -------------")
    PLAYER1=User(True)
    PLAYER2=User(False)
    #startGame()

#########GLOBALS##########

#dizionario di funzioni, come indice interi che vengono visualizzati nel menù principale
gamemodes={
    1:singleplayer_setup,
    2:multiplayer_setup
}

PLAYER1=None
PLAYER2=None
BOARD=Board()
TURN=True #true for player1, false for player2

def main():
    clearTerminal()
    print("================ TRIS ================")
    print(" 1) Singleplayer")
    print(" 2) Multiplayer\n")
    scelta=int_input(">>> Inserire modalità di gioco: ")
    while scelta not in [1,2]:
        scelta=int_input(">>> Scelta non valida. Inserire modalità di gioco: ")
    gamemodes[scelta]()
        
main()