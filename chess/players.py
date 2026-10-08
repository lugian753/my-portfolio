from abc import ABC, abstractmethod
import random

# CLASSE BASE ASTRATTA PER RAPPRESENTAZIONE GIOCATORE
class Player(ABC):

    def __init__(self, color):
        self.color = color  # 'w' per Bianco, 'b' per Nero
        self.myturn = (color == 'w') # True se Bianco (muove per primo)

    @abstractmethod
    def get_move(self, board):
        """
        Metodo astratto da implementare nelle sottoclassi User e Computer.
        Deve restituire un dizionario con i dettagli della mossa convalidata.
        """
        pass
           

class User(Player):

    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board):     
        # Generiamo le mosse legali aggiornate per questo turno
        legal_moves = board.generate_legal_moves()
        
        while True:
            print(f"\n***Turno del { 'BIANCO' if self.color == 'w' else 'NERO' }")
            user_input = input(">>> Inserisci mossa (es: e2 e4): ").strip().lower()
            parts = user_input.split()
            
            if len(parts) != 2:
                print("Formato errato! Inserisci due coordinate separate da spazio (es: e2 e4).")
                continue
            
            #traduzione di stringhe utente in indici di matrice dentro una tupla
            origin = board.coordinates_to_indexes(parts[0])
            destination = board.coordinates_to_indexes(parts[1])
            
            if origin is None or destination is None:
                print("***Coordinate fuori dalla scacchiera! Usa lettere da a-h e numeri da 1-8.")
                continue
            
            #se la mossa inserita fa parte delle mosse legali calcolate dalla Board
            if origin in legal_moves and destination in legal_moves[origin]:
                
                #identifichiamo il pezzo che l'utente vuole muovere
                piece = board.grid[origin[0]][origin[1]]
                row_o, col_o = origin
                row_d, col_d = destination
                
                #parametri di default della mossa
                en_passant = False
                castle = False
                pawn_promotion = 'p'
                
                #INTERCETTAZIONE MOSSE SPECIALI LATO UTENTE:
                
                #1) en passant (è un pedone, cambia colonna ma va in una casella vuota)
                if piece.value == 100 and col_o != col_d and board.grid[row_d][col_d] is None:
                    en_passant = True
                
                #2) arrocco (è il re e si sposta lateralmente di due caselle)
                elif piece.value == 999999 and abs(col_d - col_o) == 2:
                    castle = True
                
                #3) promozione? (è un pedone e raggiunge l'estremità opposta)
                elif piece.value == 100 and (row_d == 0 or row_d == 7):
                    while True:
                        scelta = input(">>> Promozione! Scegli il pezzo (q=Regina, r=Torre, b=Alfiere, n=Cavallo): ").strip().lower()
                        if scelta in ['q', 'r', 'b', 'n']:
                            pawn_promotion = scelta
                            break
                        print(">>> Scelta non valida! Inserisci q, r, b oppure n.")
                
                #se la mossa supera tutti i controlli, restituiamo un dizionario completo!
                return {
                    'origin': origin,
                    'destination': destination,
                    'en_passant': en_passant,
                    'castle': castle,
                    'pawn_promotion': pawn_promotion
                }
            else:
                print("Mossa non legale per questo pezzo! Riprova.")


class Computer(Player):
    def __init__(self, color):
        super().__init__(color)

    def get_move(self, board):
        """
        Sceglie una mossa completamente casuale tra quelle legali disponibili.
        Restituisce lo stesso dizionario formattato richiesto da insert_move.
        """
        print(f"\n[Il COMPUTER ({'BIANCO' if self.color == 'w' else 'NERO'}) sta pensando...]")
        
        #recuperiamo tutte le mosse legali attuali della scacchiera
        legal_moves = board.generate_legal_moves()
        
        #sicurezza: se non ci sono mosse (scacco matto o stallo), restituisce None
        #anche se teoricamente il ciclo principale si interrompe prima
        if not legal_moves:
            return None

        #selezioniamo una casella di partenza (chiave) a caso tra i pezzi che possono muoversi
        origin = random.choice(list(legal_moves.keys()))
        
        #selezioniamo una destinazione a caso tra quelle possibili per quel pezzo
        destination = random.choice(legal_moves[origin])
        
        #intercettiamo se la mossa casuale scelta è una mossa speciale
        piece = board.grid[origin[0]][origin[1]]
        row_o, col_o = origin
        row_d, col_d = destination
        
        en_passant = False
        castle = False
        pawn_promotion = 'p'
        
        #controlli geometrie mosse speciali per il Bot
        if piece.value == 100 and col_o != col_d and board.grid[row_d][col_d] is None:
            en_passant = True
        elif piece.value == 999999 and abs(col_d - col_o) == 2:
            castle = True
        elif piece.value == 100 and (row_d == 0 or row_d == 7):
            pawn_promotion = 'q'

        return {
            'origin': origin,
            'destination': destination,
            'en_passant': en_passant,
            'castle': castle,
            'pawn_promotion': pawn_promotion
        }