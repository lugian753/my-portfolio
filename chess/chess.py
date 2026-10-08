
from utils import *
from board import *
from players import *


TITLE = "=========================== SCACCHI ==========================="




class Game:
    def __init__(self):
        self.board = Board()
        self.turn = True 
        self.gamemodes = {
            1: self.singleplayer_setup,
            2: self.multiplayer_setup,
        }

    
    def singleplayer_setup(self):
        scelta = int_input(">>> Chi parte (1 PC 2 Utente): ")
        while scelta not in (1,2):
            scelta = int_input(">>> Scelta non valida. Chi parte (1 PC 2 Utente): ")
        if scelta == 1:
            self.player1 = Computer('w')
            self.player2 = User('b')
        else:
            self.player1 = User('w')
            self.player2 = Computer('b')
        self.start_game()

    def multiplayer_setup(self):
        self.player1 = User('w')
        self.player2 = User('b')
        self.start_game()

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

    def start_game(self):
        clear_terminal()
        print("Inizializzazione della scacchiera...")
        self.board.starting_position()
        self.turn = self.board.turn 

        while self.board.game_state == 'n':
            clear_terminal()
            print(TITLE)
            self.board.view_board()
            current_player = self.player1 if self.board.turn else self.player2
            move = current_player.get_move(self.board)
            
            self.board.insert_move(
                origin=move['origin'],
                destination=move['destination'],
                en_passant=move['en_passant'],
                castle=move['castle'],
                pawn_promotion=move['pawn_promotion']
            )
            self.board.calculate_game_state()

        clear_terminal()
        print(TITLE)
        self.board.view_board()
        print("\n=== FINE PARTITA ===")
        
        if self.board.game_state == 'd':
            print("***La partita è terminata in PATTA!")
        else:
            vincitore = "BIANCO" if self.board.game_state == 'w' else "NERO"
            print(f"*** SCACCO MATTO! Il giocatore {vincitore} ha vinto la partita!")
            
        input("\nPremere Invio per tornare al menu principale...")

        self.board.game_state = 'n'

    def game_main(self):
            #main del gioco, apre il menu principale e chiama i metodi in base alla modalità selezionata
            while True:
                scelta = self.menu_principale()
                if scelta == 3:
                    break
                self.gamemodes[scelta]()

def main():
    game = Game()
    game.game_main()


if __name__ == "__main__":
    main()

