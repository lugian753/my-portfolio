from pieces import *

class Board:

    turn = True #white moves first
    game_state = 'n' #n: partita in corso, w: vittoria bianco, b: vittoria nero, d: patta
    quiet_moves = 0
    
    def __init__(self):
        self.grid = [ 
            [None for _ in range(8) ], 
            [None for _ in range(8) ],  
            [None for _ in range(8) ],  
            [None for _ in range(8) ],  
            [None for _ in range(8) ],  
            [None for _ in range(8) ],  
            [None for _ in range(8) ],  
            [None for _ in range(8) ] 
        ]
        self.move_history = []
        self.positions_history = {}
        
   
    def coordinates_to_indexes(self, coordinates):
        if len(coordinates) != 2:
            return None
        
        #in chess notation column first instead of row
        col_char, row_char = coordinates[0], coordinates[1]

        if col_char not in "abcdefgh" or row_char not in "12345678":
            return None
        
        row = 8 - int(row_char)
        col = ord(col_char) - ord('a') #sfrutto codifica unicode
        return (row, col)

    def starting_position(self):
        #popolazione della scacchiera con istanze dei pezzi
        self.grid[0] = [Rook('b', 0, 0), Knight('b', 0, 1), Bishop('b', 0, 2), Queen('b', 0, 3), King('b', 0, 4), Bishop('b', 0, 5), Knight('b', 0, 6), Rook('b', 0, 7)]
        self.grid[1] = [Pawn('b', 1, i) for i in range(8)]
        self.grid[6] = [Pawn('w', 6, i) for i in range(8)]
        self.grid[7] = [Rook('w', 7, 0), Knight('w', 7, 1), Bishop('w', 7, 2), Queen('w', 7, 3), King('w', 7, 4), Bishop('w', 7, 5), Knight('w', 7, 6), Rook('w', 7, 7)]

    def generate_pseudolegal_moves(self):
            moves = {}
            color_to_move = 'w' if self.turn else 'b'
            for rows in self.grid:
                for piece in rows:
                    if piece is not None and piece.color == color_to_move:
                        moves[(piece.row, piece.col)] = piece.generate_moves(self.grid)
            return moves

    def insert_move(self, origin, destination, en_passant=False, castle=False, pawn_promotion='p'):
        #origin e destination saranno sempre 2 tuple valide
        #pawn_promotion conterrà "p" in qualsiasi mossa oppure un carattere che identifica a quale pezzo promuovere
        #q = regina, n = cavallo, r = torre, b = alfiere

        
        row_o, col_o = origin[0], origin[1]
        row_d, col_d = destination[0], destination[1] #coordinate salvate

        piece = self.grid[row_o][col_o]

        if piece is None:
            return False

        #due etichette per l'undo_move e gestione mosse speciali
        special_move_type = 'normal'
        extra_data = None
        
        #per rollback per calcolare mosse legali o permettere all'utente di tornare indietro
        target_piece = self.grid[row_d][col_d]

        #reset dei flag en passant dei pedoni alleati all'inizio del turno
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None and p.color == piece.color and p.value == 100:
                    p.has_just_moved_by_2 = False

        #gestione mosse speciali
        if en_passant:
            special_move_type = 'en_passant'
            target_piece = self.en_passant(origin, destination)
        elif castle:
            extra_data = self.castle(origin, destination)        

        old_piece_state = piece.update_pos(row_d, col_d)    #si aggiorna e restituisce vecchio stato

        move_data = {
            'origin': origin,
            'destination': destination,
            'captured_piece': target_piece,
            'old_piece_state': old_piece_state,
            'special_move_type': special_move_type,
            'extra_data': extra_data
        }

        #se c'era una promozione, crea la nuova istanza del pezzo scelto
        if special_move_type == 'promotion':
            color = piece.color
            if pawn_promotion == 'q': piece = Queen(color, row_d, col_d)
            elif pawn_promotion == 'r': piece = Rook(color, row_d, col_d)
            elif pawn_promotion == 'b': piece = Bishop(color, row_d, col_d)
            elif pawn_promotion == 'n': piece = Knight(color, row_d, col_d)

        self.move_history.append(move_data)

        #commit mossa su matrice
        self.grid[row_d][col_d] = piece
        self.grid[row_o][col_o] = None


        self.turn = not self.turn
        self.quiet_moves += 1
        self.update_positions_history()

        return True

    def undo_move(self):
        if len(self.move_history) == 0:
            return False

        last_move = self.move_history.pop()
        row_o, col_o = last_move['origin']
        row_d, col_d = last_move['destination']
        special_type = last_move['special_move_type']
        extra = last_move['extra_data']

        piece = self.grid[row_d][col_d]

        #annullamento movimento base
        self.grid[row_o][col_o] = piece
        self.grid[row_d][col_d] = None

        if piece is not None:
            #se era una promozione, forziamo il pezzo a tornare un pedone
            if special_type == 'promotion':
                piece = Pawn(piece.color, row_o, col_o)
                self.grid[row_o][col_o] = piece
                
            piece.row = row_o
            piece.col = col_o
            for flag_name, flag_value in last_move['old_piece_state'].items():
                #reinserimento vecchi flag
                setattr(piece, flag_name, flag_value)

        #annullamento delle logiche specifiche dei pezzi catturati
        if special_type == 'normal' or special_type == 'promotion':
            self.grid[row_d][col_d] = last_move['captured_piece']
            
        elif special_type == 'en_passant':
            #il pedone mangiato torna sulla sua riga a fianco del tuo
            self.grid[row_o][col_d] = last_move['captured_piece']
            
        elif special_type == 'castle':
            #rimettere a posto la torre dell'arrocco usando i dati extra
            r_row_o, r_col_o = extra['rook_origin']
            r_row_d, r_col_d = extra['rook_destination']
            rook = self.grid[r_row_d][r_col_d]
            self.grid[r_row_o][r_col_o] = rook
            self.grid[r_row_d][r_col_d] = None
            if rook:
                rook.row = r_row_o
                rook.col = r_col_o
                for flag_name, flag_value in extra['old_rook_state'].items():
                    setattr(rook, flag_name, flag_value)

        self.turn = not self.turn

        #gestione sicura della rimozione della posizione corrente dallo storico delle patte
        fen_position = self.generate_fen().split(" ")
        position = " ".join(fen_position[:4])
        
        if position in self.positions_history:
            self.positions_history[position] -= 1
            if self.positions_history[position] == 0:
                del self.positions_history[position]

        self.quiet_moves -= 1
        return True

    def en_passant(self, origin, destination):
        #gestisce la logica della cattura en passant.
        #cancella il pedone avversario e restituisce l'oggetto pezzo eliminato per l'history.
        row_o, col_o = origin
        row_d, col_d = destination

        #nell'en passant, il pedone avversario non si trova sulla casella di destinazione,
        #ma sulla stessa riga di partenza (row_o) e sulla colonna di arrivo (col_d).
        captured_piece = self.grid[row_o][col_d]
        
        #rimuoviamo fisicamente il pedone avversario dalla matrice
        self.grid[row_o][col_d] = None
        
        #restituiamo il pezzo eliminato a insert_move, così verrà salvato correttamente 
        #rella chiave 'captured_piece' del dizionario di rollback
        return captured_piece

    def generate_legal_moves(self):
        legal_moves = {}
        pseudo_legal = self.generate_pseudolegal_moves()
        player_to_move = 'w' if self.turn else 'b'
        promotion_choices = ['q', 'r', 'b', 'n'] #necessario
        for row in self.grid:
            for piece in row:
                if piece is not None and piece.color == player_to_move: #quando trovo pezzo del colore corretto
                    origin = piece.get_pos()    #posizione del pezzo
                    moves = []      #inizializzo lista mosse legali del singolo pezzo

                    if origin not in pseudo_legal:
                        continue #se il pezzo non ha nessuna mossa legale, skip
                
                    for destination in pseudo_legal[origin]:
                        row_o, col_o = origin
                        row_d, col_d = destination

                        #CONTROLLO SPECIALE ARROCCO
                        is_castle = (piece.value == 999999 and abs(col_d - col_o) == 2)
                        if is_castle:
                            #regola 1) non si può arroccare if si è già sotto scacco
                            if self.king_under_attack(player_to_move):
                                continue
                            
                            #regola 2) il re non può attraversare una casa sotto attacco
                            #colonna 5 per l'arrocco corto, colonna 3 per il lungo
                            transit_col = 5 if col_d == 6 else 3
                            transit_destination = (row_o, transit_col)
                            
                            #muoviamo temporaneamente il re solo sulla casa di transito
                            self.insert_move(origin, transit_destination)
                            is_transit_unsafe = self.king_under_attack(player_to_move)
                            self.undo_move()
                            
                            if is_transit_unsafe:
                                continue #se la casella di transito è sotto attacco, l'arrocco salta

                        pawn_is_promoting = (piece.value == 100 and ((piece.color == 'w' and row_d == 0) or (piece.color == 'b' and row_d == 7)))

                        if pawn_is_promoting:
                            #se è una promozione vanno simulate tutte e 4 le varianti possibili
                            for choice in promotion_choices:
                                #passiamo il carattere del pezzo scelto a insert_move
                                self.insert_move(origin, destination, pawn_promotion=choice)
                                if not self.king_under_attack(player_to_move): #se non è sotto scacco
                                    if destination not in moves:
                                        moves.append(destination)
                                self.undo_move()
                        else:
                            #MOSSA STANDARD (E VERIFICA FINALE ARROCCO)
                            #se è un arrocco superato il controllo di transito, passare castle=True
                            self.insert_move(origin, destination, castle=is_castle)
                            if not self.king_under_attack(player_to_move):
                                moves.append(destination)
                            self.undo_move() 
                    if moves:
                        #solo se il pezzo ha almeno una mossa legale a disposizione
                        legal_moves[origin] = moves #dizionario[coordinate pezzo] = [lista di coordinate destinazioni legali]
        return legal_moves

    def castle(self, origin, destination):
        #sposta fisicamente la torre durante l'arrocco e restituisce i suoi dati storici
        row_o, col_o = origin
        row_d, col_d = destination

        #capire se si tratta di un arrocco corto (colonna d'arrivo 6) o lungo (colonna d'arrivo 2)
        is_kingside = (col_d == 6)
        rook_col_o = 7 if is_kingside else 0
        rook_col_d = 5 if is_kingside else 3

        #prendere la torre dalla sua casa originaria
        rook = self.grid[row_o][rook_col_o]
        
        #spostamento fisico la torre sulla grid
        self.grid[row_o][rook_col_d] = rook
        self.grid[row_o][rook_col_o] = None
        
        #aggiornia coordinate della torre e cattura i suoi vecchi flag per l'undo
        old_rook_state = rook.update_pos(row_o, rook_col_d) if rook else None

        #restituire i dati a insert_move affinché valorizzi la chiave 'extra_data' della history
        return {
            'rook_origin': (row_o, rook_col_o),
            'rook_destination': (row_o, rook_col_d),
            'old_rook_state': old_rook_state
        }

    def promotion(self, origin, destination, piece_type):
        #fase iniziale della promozione di un pedone
        row_d, col_d = destination[0], destination[1]
        
        #recuperare l'eventuale pezzo avversario catturato sulla casella di arrivo, fondamentale per rollback
        captured_piece = self.grid[row_d][col_d]
        
        #extra_data conterrà il carattere ('q', 'r', 'b', 'n') scelto per la promozione.
        return {
            'captured_piece': captured_piece,
            'special_move_type': 'promotion',
            'extra_data': {'promoted_to': piece_type}
        }

    def king_under_attack(self, color):
        """Controlla se il Re del colore specificato è sotto scacco."""
        # 1. Trova le coordinate del Re del colore richiesto
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                # Controlliamo il valore del Re (999999) e il colore
                if p is not None and p.value == 999999 and p.color == color:
                    king_pos = p.get_pos() # Usiamo il tuo get_pos()
                    break
            if king_pos:
                break

        if not king_pos:
            return False # Se il re non c'è, non è sotto scacco

        # 2. Chi è l'attaccante? 
        # Se controlliamo il Re Bianco ('w'), l'attaccante è il Nero ('b') e viceversa.
        attacker_color = 'b' if color == 'w' else 'w'

        # 3. Forziamo il turno sull'attaccante per generare le sue mosse
        original_turn = self.turn
        self.turn = (attacker_color == 'w') # True se attacca il bianco, False se attacca il nero
        
        opponent_moves = self.generate_pseudolegal_moves()
        
        # Ripristiniamo IMMEDIATAMENTE il turno originale
        self.turn = original_turn

        # 4. Verifichiamo se la posizione del Re è tra le destinazioni dell'attaccante
        for _, destinations in opponent_moves.items():
            if king_pos in destinations:
                return True # Il Re è sotto scacco!
                
        return False

    def update_positions_history(self):
        #conversione da stringa fen standard a stringa fen con solo i primi 4 campi, quelli utili per la patta per ripetizione
        fen_position = self.generate_fen().split(" ")
        fen_position = fen_position[:4]
        position = " ".join(fen_position)

        #registro nel dizionario se non esiste o incremento se c'è già
        self.positions_history[position] = self.positions_history.get(position, 0) + 1

    def calculate_game_state(self):

        player_to_move = 'w' if self.turn else 'b'

        if not self.generate_legal_moves():
            if self.king_under_attack(player_to_move):
                #colori invertiti perchè chi non ha mosse non ha vinto ma ha perso
                self.game_state = 'b' if self.turn else 'w'
                return self.game_state
            else:
                #stallo
                self.game_state = 'd'
                return self.game_state

        #altre condizioni di patta:
        #1) materiale insufficiente: nessun pedone sulla scacchiera e meno di 500 punti valore totali per colore (escluso il re)
                                                                            #500 = una torre e < di 2 pezzi leggeri
        #2) regola delle 50 mosse: se per 50 mosse consecutive non viene catturato un pezzo e nessun pedone viene mosso: patta

        #3) patta per ripetizione: se una posizione si ripete 3 volte è patta: implementazione semplice: dizionario[posizione]=count

        #condizione 1)
        w_value = 0
        b_value = 0
        pawns = False
        for row in self.grid:
            for piece in row:
                if piece and piece.value == 100:
                    pawns = True
                    break #pedone trovato, materiale sufficiente
                elif piece and piece.value > 900 and piece.color == 'w': #ignora i re e incrementa somma w
                    w_value += piece.value
                elif piece and piece.value > 900 and piece.color == 'b': #ignora i re e incrementa somma b
                    b_value += piece.value
        if not pawns and w_value < 500 and b_value < 500:
            #materiale insufficiente
            self.game_state = 'd'
            return self.game_state

        #condizione 2)
        if self.quiet_moves >= 100:
            self.game_state = 'd'
            return self.game_state

        #condizione 3) controllo sulla posizione attuale, il metodo verrà chiamato dopo ogni mossa
        current_position = " ".join(self.generate_fen().split(" ")[:4])

        if self.positions_history.get(current_position, 0) >= 3:
            self.game_state = 'd'
            return self.game_state

        #nessun vincitore, nessuna condizione di patta soddisfatta, partita ancora in corso
        self.game_state = 'n'
        return self.game_state

    def view_board(self):
        print("\n    A   B   C   D   E   F   G   H")
        print(  "  +---+---+---+---+---+---+---+---+")
        for i, row in enumerate(self.grid):
            row_n = 8 - i  #conversione da indice a numero delle coordinate della scacchiera
            print(f"{row_n} |", end="")
            for piece in row:
                if piece is not None:
                    print(f" {piece.unicode} |", end="")
                else:
                    print("   |", end="")
            print(f" {row_n}")
            print("  +---+---+---+---+---+---+---+---+")
        print(    "    A   B   C   D   E   F   G   H\n")


    def generate_fen(self):
        #genera la stringa FEN ufficiale completa (6 campi) per lo stato attuale
        #CAMPO 1: posizionamento dei pezzi
        fen_ranks = []
        piece_symbols = {
            'Pawn': 'p', 'Rook': 'r', 'Knight': 'n', 
            'Bishop': 'b', 'Queen': 'q', 'King': 'k'
        }   #non posso usare il valore dei pezzi perchè cavallo e alfiere valgono entrambi 300
        #certo potrei sempre mettere alfiere a 301 e cavallo a 299, dopotutto molti concordano sul fatto
        #che in realtà l'alfiere sia lievemente più forte del cavallo ma preferisco tenere la struttura con 
        #valori standard, uso quindi il nome delle classi come chiavi
        
        for row in self.grid:
            empty_squares = 0
            rank_str = ""
            for piece in row:
                if piece is None:
                    empty_squares += 1
                else:
                    #se c'erano caselle vuote accumulate scrive il numero prima del pezzo
                    if empty_squares > 0:
                        rank_str += str(empty_squares)
                        empty_squares = 0
                    
                    class_name = piece.__class__.__name__ #nome della classe del pezzo in class_name
                    char = piece_symbols[class_name]
                    rank_str += char.upper() if piece.color == 'w' else char.lower() #bianco maiuscolo e nero minuscolo
            
            if empty_squares > 0:
                rank_str += str(empty_squares)
            fen_ranks.append(rank_str)   

        pieces_field = "/".join(fen_ranks)

        #CAMPO 2: turno
        turn_field = 'w' if self.turn else 'b'

        #CAMPO 3: diritti di arrocco (castling rights)
        #cerchiamo i re e le torri per vedere se si sono mai mossi (has_moved)
        castle_str = ""
        
        #bianco
        w_king = self.grid[7][4]
        if w_king and w_king.__class__.__name__ == 'King' and not w_king.has_moved:
            w_rook_k = self.grid[7][7] # Torre lato Re
            w_rook_q = self.grid[7][0] # Torre lato Donna
            if w_rook_k and w_rook_k.__class__.__name__ == 'Rook' and not w_rook_k.has_moved:
                castle_str += "K"
            if w_rook_q and w_rook_q.__class__.__name__ == 'Rook' and not w_rook_q.has_moved:
                castle_str += "Q"
                
        #nero
        b_king = self.grid[0][4]
        if b_king and b_king.__class__.__name__ == 'King' and not b_king.has_moved:
            b_rook_k = self.grid[0][7]
            b_rook_q = self.grid[0][0]
            if b_rook_k and b_rook_k.__class__.__name__ == 'Rook' and not b_rook_k.has_moved:
                castle_str += "k"
            if b_rook_q and b_rook_q.__class__.__name__ == 'Rook' and not b_rook_q.has_moved:
                castle_str += "q"
                
        castle_field = castle_str if castle_str else "-"


        #CAMPO 4: en passant
        #cerca pedone che ha appena fatto il doppio passo
        ep_field = "-"
        #se tocca al bianco, cerca un pedone nero che ha appena saltato sulla riga indice 3
        #se tocca al nero, cerca un pedone bianco sulla riga indice 4
        target_row = 3 if self.turn else 4
        opp_color = 'b' if self.turn else 'w'
        
        for c in range(8):
            p = self.grid[target_row][c]
            if p is not None and p.value == 100 and p.color == opp_color:
                
                if p.has_just_moved_by_2: #controllo flag
                    #calcolo della casa dietro di lui in notazione scacchistica
                    col_char = chr(ord('a') + c)
                    row_char = "3" if self.turn else "6"
                    ep_field = f"{col_char}{row_char}"
                    break

        #CAMPI 5 e 6: regola 50 mosse e numero mossa corrente
        halfmove_clock = str(self.quiet_moves)
        fullmove_number = str(1 + (len(self.move_history) // 2)) #il numero di mosse totali inizia da 1 e aumenta dopo ogni mossa del nero

        return f"{pieces_field} {turn_field} {castle_field} {ep_field} {halfmove_clock} {fullmove_number}"
