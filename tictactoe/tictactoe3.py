from abc import ABC, abstractmethod
from utils import clear_terminal ,int_input

TITLE =         "================ TRIS ================"
MULTIPLAYER =   "              MULTIPLAYER"
SINGLEPLAYER =  "             SINGLEPLAYER"

class Board:
    moves_matrix = {
        0: (0, 0), 1: (0, 1), 2: (0, 2),
        3: (1, 0), 4: (1, 1), 5: (1, 2),
        6: (2, 0), 7: (2, 1), 8: (2, 2)
    } #dizionario per tradurre la mossa inserita dall'utente come intero negli indici della matrice

    def __init__(self):
        self.clear_board()   

    #stampa board e affianco i numeri che identificano ogni casa della board
    def view_board(self):
        for i, row in enumerate(self.board):
            if i != 0:
                print("---+---+---", end="")
                print("\t" * 4 + "---+---+---")
            for j, square in enumerate(row):
                if j != 0:
                    print(" |", end="")

                print(f" {square}", end="")
            print("\t" * 4 + f" {i * 3} | {i * 3 + 1} | {i * 3 + 2}")
        print("")#per andare a capo di una riga in più

    #reinizializzazione istanza
    def clear_board(self):
        self.board=[
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ] #la scacchiera viene definita come matrice, ogni spazio indica la posizione libera,
        #altrimenti conterrà il carattere del giocatore (X o O)            
        self._update_available_moves() #lista interi mosse corrispondenti a elemento matrice vuoto

    #aggiorna la lista e la ritorna
    def _update_available_moves(self):
        self.available_moves = [slot for slot, (row, col) in self.moves_matrix.items() if self.board[row][col] == ' ']

    #false if mossa non inserita else true
    def insert_move(self, player, move):
        if move not in self.available_moves:
            return False
        x, y = self.moves_matrix[move]
        self.board[x][y] = player
        self._update_available_moves()
        return True

    #return 'X' se X ha vinto, 'O' se O ha vinto, 'D' se è finita in pareggio, 'N' se la partita è in corso
    def game_winner(self):
        #controllo orizzontali
        for row in self.board:
            if row[0] == row[1] and row[1] == row[2] and row[2] != ' ':
                return row[2]

        #controllo verticali
        for i in range(3):
            if self.board[0][i] == self.board[1][i] and self.board[1][i] == self.board[2][i] and self.board[2][i] != ' ':
                return self.board[2][i]

        #controllo diagonali
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[2][2] != ' ':
            return self.board[2][2]

        if self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2] and self.board[0][2] != ' ':
            return self.board[0][2]

        #non ci sono vittorire sulla board, se non ci sono mosse disponibili allora è pareggio se no la partita è in corso
        if len(self.available_moves) > 0:
            return 'N'
        return 'D'

    def undo_move(self, move):
        if move not in self.available_moves:
            x, y = self.moves_matrix[move]
            self.board[x][y] = ' '
            self._update_available_moves()


#classe base astratta per rappresentazione giocatore
class Player(ABC):

    def __init__(self, myturn):
        self.sign = "X" if myturn else "O"
        self.myturn = myturn

    @abstractmethod
    def get_move(self, board):
        #metodo astratto da implementare nelle sottoclassi User e Computer
        #restituisce un intero da 0 a 8
        pass


class Computer(Player):

    def __init__(self, myturn):
        super().__init__(myturn)
        self.opponent = 'O' if myturn else 'X'

    def minimax(self, board, myturn, alpha, beta):
        game_state = board.game_winner()
        match game_state:
            case self.sign:
                return 1
            case self.opponent:
                return -1
            case 'D':
                return 0

        #best_score = -10 if myturn else 10 #worse than worst for both players
        #best_score sostituita da alpha e beta
        best_score = alpha if myturn else beta
        sign = self.sign if myturn else self.opponent

        for m in list(board.available_moves):
            board.insert_move(sign, m)
            score = self.minimax(board, not myturn, alpha, beta)
            #undoing move
            board.undo_move(m)

            #vittorie e sconfitte
            if myturn and score == 1:
                return 1
            elif not myturn and score == -1:
                return -1
            
            #pareggi e in corso
            elif myturn and score > best_score:
                best_score = score
                alpha = score #update alpha
            elif not myturn and score < best_score:
                best_score = score
                beta = score #update beta

            if alpha >= beta:
                break

        return best_score


    def get_move(self, board):
        best_score = -10 #worse than worst possible
        best_move = -1 #non existing move

        #alpha beta pruning
        alpha, beta = -10, +10

        for m in list(board.available_moves):
            board.insert_move(self.sign, m)
            score = self.minimax(board, False, alpha, beta)
            #undoing changes on board
            board.undo_move(m)
            if score > best_score:
                best_score = score
                alpha = score   #alpha beta pruning
                best_move = m
                #piccola ottimizzazione
                if best_score == 1:
                    break
                #inutile continui a cercare se ha la certezza di vincere
        return best_move
            


class User(Player):

    def __init__(self, myturn):
        super().__init__(myturn)
        self.helper = Computer(myturn)

    def get_move(self, board):     
        while True:
            mossa = int_input(">>> Inserisci mossa o 9 per chiedere aiuto al computer: ")
            if mossa in board.available_moves:
                return mossa
            if mossa == 9:
                print(f"*** MOSSA CONSIGLIATA: {self.helper.get_move(board)}")
            else:
                print(">>> Mossa illegale o non esitente. ", end='')


class GameManager:

    def __init__(self):    
        self.board = Board()
        self.turn = True

        self.gamemodes = {
            1: self.singleplayer_setup,
            2: self.multiplayer_setup,
        }

    def singleplayer_setup(self):
        clear_terminal()
        print(TITLE)
        print("\n***CHI INIZIA?")
        print(" 1) Computer")
        print(" 2) Utente")
        scelta = int_input("\n>>> Inserire scelta: ")
        while scelta not in (1, 2):
            scelta = int_input("\n>>> Scelta non valida. Inserire scelta: ")
        if scelta == 1:
            self.player1 = Computer(True)
            self.player2 = User(False)
        else:
            self.player1 = User(True)
            self.player2 = Computer(False)
        modalità = SINGLEPLAYER
        self.start_game(modalità)

    #inizializzo i player e parte il gioco
    def multiplayer_setup(self):
        self.player1 = User(True)
        self.player2 = User(False)
        modalità = MULTIPLAYER
        self.start_game(modalità)

    #stabilisco i turni dei giocatori con un booleano, il metodo game winner controlla che la partita sia ancora in corso
    def start_game(self, mode):
        turn = True
        judge = Computer(myturn=True)   #valuta posizione
        self.board.clear_board()    #reinizializza board
        while self.board.game_winner() == "N":
            current_player = self.player1 if turn else self.player2

            eval = judge.minimax(self.board, turn, alpha=-10, beta=10)  #valutazione posizione       
            
            clear_terminal()    #stampa stato board
            print(TITLE)
            print(mode)
            self.board.view_board()

            print("\n*** VALUTAZIONE POSIZIONE: ", end='')  #stampa valutazione (pareggio oppure vittoria di uno dei giocatori)
            if eval == 0:
                print("PAREGGIO CON GIOCO CORRETTO")   
            else:    
                print((f"{judge.sign} " if eval == 1 else f"{judge.opponent} ") + "VINCE CON GIOCO CORRETTO")

            print(f"*** TOCCA A {current_player.sign}") #input next move
            move = current_player.get_move(self.board)
            self.board.insert_move(current_player.sign, move)

            turn = not turn #cambio turno          

        winner = self.board.game_winner()
        clear_terminal()
        print(TITLE)
        print(mode)
        self.board.view_board()
        if winner != 'D':
            print(f"*** {winner} HA VINTO! ****")
        else:
            print("*** PAREGGIO! ***")
        input(">>> Premere invio per continuare ...")


    def menu_principale(self):
        clear_terminal()
        print(TITLE)
        print(" 1) Singleplayer")
        print(" 2) Multiplayer")
        print(" 3) Esci\n")
        scelta = int_input(">>> Inserire scelta: ")
        while scelta not in [1, 2, 3]:
            scelta = int_input(">>> Opzione non valida. Inserire scelta: ")
        return scelta

    def game_main(self):
        #main del gioco, apre il menu principale e chiama i metodi in base alla modalità selezionata
        while True:
            scelta = self.menu_principale()
            if scelta == 3:
                break
            self.gamemodes[scelta]()



def main():
    game = GameManager()
    game.game_main()
    

if __name__ == "__main__":
    main()