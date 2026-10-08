from abc import ABC, abstractmethod

#CLASSE BASE ASTRATTA PER I PEZZI
class Piece(ABC):
    def __init__(self, color, row, col):
        self.color = color      #w per bianco, b per nero
        self.has_moved = False  #per re e torri per gli arrocchi, e per pedoni
        self.unicode = self._assign_unicode()
        self.row = row
        self.col = col

    @abstractmethod
    def _assign_unicode(self):
        pass

    @abstractmethod
    def generate_moves(self, grid):
        pass

    def get_pos(self):
        return (self.row, self.col)

    def update_pos(self, new_row, new_col):
        #salva lo stato precedente generico
        old_state = {'has_moved': self.has_moved}
        
        self.row = new_row
        self.col = new_col
        self.has_moved = True     
        return old_state

########## PEZZI

class Pawn(Piece):
    value = 100 #pedone vale 1 (moltiplico per 100 per valutazione più precisa)

    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.has_just_moved_by_2 = False #serve per en passant

    def _assign_unicode(self):
        return "♙" if self.color == 'w' else "♟"

    def generate_moves(self, grid):
        moves = []
        row_change = -1 if self.color == 'w' else +1
        next_row = self.row + row_change

        if not 0 <= self.row + row_change <= 7:
            return moves 

        #movimenti di 1
        if grid[next_row][self.col] is None:
            moves.append((next_row, self.col))

            #movimenti di 2
            next_row = self.row + row_change * 2
            if not self.has_moved and grid[next_row][self.col] is None:
                moves.append((next_row, self.col))

        #catture a destra
        if self.col != 7:   
            target = grid[next_row][self.col + 1]
            if target is not None and target.color != self.color:
                moves.append((next_row, self.col + 1))

        #catture a sinistra
        if self.col != 0:   
            target = grid[next_row][self.col - 1]
            if target is not None and target.color != self.color:
                moves.append((next_row, self.col - 1))

        #cattura en passant a destra
        if self.col != 7:   
            neighbor = grid[self.row][self.col + 1]
            if neighbor is not None and neighbor.color != self.color and neighbor.value == 100:
                if hasattr(neighbor, 'has_just_moved_by_2') and neighbor.has_just_moved_by_2:
                    moves.append((next_row, self.col + 1))     
       
        #cattura en passant a sinistra
        if self.col != 0:   
            neighbor = grid[self.row][self.col - 1]
            if neighbor is not None and neighbor.color != self.color and neighbor.value == 100:
                if hasattr(neighbor, 'has_just_moved_by_2') and neighbor.has_just_moved_by_2:
                    moves.append((next_row, self.col - 1))     

        return moves

    def update_pos(self, new_row, new_col):
        #salva sia il suo has_moved sia il flag dell'en passant per consentire l'undo_move
        old_state = {
            'has_moved': self.has_moved,
            'has_just_moved_by_2': self.has_just_moved_by_2
        }
        
        #logica del doppio passo gestita dal pedone stesso
        if abs(new_row - self.row) == 2:
            self.has_just_moved_by_2 = True
        else:
            self.has_just_moved_by_2 = False
            
        self.row = new_row
        self.col = new_col
        self.has_moved = True
        
        return old_state


class Rook(Piece):

    value = 500 #5 pedoni, meno di 2 pezzi leggeri, più della metà della regina ( 2 torri > 1 regina )

    def _assign_unicode(self):
        return "♖" if self.color == 'w' else "♜"

    def generate_moves(self, grid):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]   

        for dir_row, dir_col in directions:
            a, b = self.row + dir_row, self.col + dir_col   #non voglio alterare la posizione del pezzo
            while 0 <= a < 8 and 0 <= b < 8:             
                neighbor = grid[a][b]
                if neighbor is None:
                    moves.append((a, b))
                else:
                    if neighbor.color != self.color:
                        moves.append((a, b))
                    break
                a += dir_row
                b += dir_col
        return moves

        
class Bishop(Piece):

    value = 300 #pezzo leggero, 3 di essi == 1 regina

    def _assign_unicode(self):
        return "♗"if self.color == 'w' else "♝"

    def generate_moves(self, grid):
        moves = []
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]   

        for dir_row, dir_col in directions:
            a, b = self.row + dir_row, self.col + dir_col   #non voglio alterare la posizione del pezzo
            while 0 <= a < 8 and 0 <= b < 8:             
                neighbor = grid[a][b]
                if neighbor is None:
                    moves.append((a, b))
                else:
                    if neighbor.color != self.color:
                        moves.append((a, b))
                    break
                a += dir_row
                b += dir_col
        return moves


class Knight(Piece):

    value = 300 #pezzo leggero, 3 di essi == 1 regina

    def _assign_unicode(self):
        return "♘" if self.color == 'w' else "♞"

    def generate_moves(self, grid):
        moves = []
        directions = [
            (-2, -1),   (-2, +1),
          (-1, -2),        (-1, +2),
                    #self
          (+1, -2),        (+1, +2),
            (+2, -1),   (+2, +1)
        ]
        for dir_row, dir_col in directions:
            a, b = self.row + dir_row, self.col + dir_col
            if 0 <= a < 8 and 0 <= b < 8:
                neighbor = grid[a][b]
                if neighbor is None or neighbor.color != self.color:
                    moves.append((a, b))
        return moves


class Queen(Piece):

    value = 900 #come 3 pezzi leggeri, meno di 2 torri

    def _assign_unicode(self):
        return "♕" if self.color == 'w' else "♛"

    def generate_moves(self, grid):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]   

        for dir_row, dir_col in directions:
            a, b = self.row + dir_row, self.col + dir_col   #non voglio alterare la posizione del pezzo
            while 0 <= a < 8 and 0 <= b < 8:             
                neighbor = grid[a][b]
                if neighbor is None:
                    moves.append((a, b))
                else:
                    if neighbor.color != self.color:
                        moves.append((a, b))
                    break
                a += dir_row
                b += dir_col
        return moves


class King(Piece):

    value = 999999 #non in termini di utilità ma va protetto a tutti i costi

    def _assign_unicode(self):
        return "♔" if self.color == 'w' else "♚"

    def generate_moves(self, grid):
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dir_row, dir_col in directions:
            a, b = self.row + dir_row, self.col + dir_col
            if 0 <= a < 8 and 0 <= b < 8:
                neighbor = grid[a][b]
                if neighbor is None or neighbor.color != self.color:
                    moves.append((a, b))

        #LOGICA DELL'ARROCCO
        if not self.has_moved:
            #ARROCCO CORTO
            #controllo se all'estremo destro c'è la torre
            right_rook = grid[self.row][7]
            if right_rook is not None and right_rook.value == 500 and not right_rook.has_moved: #la torre non deve essersi mossa
                #le case in mezzo (colonne 5 e 6) devono essere libere
                if grid[self.row][5] is None and grid[self.row][6] is None:
                    moves.append((self.row, 6))

            #ARROCCO LUNGO)
            #controllo se all'estremo sinistro c'è la torre
            left_rook = grid[self.row][0]
            if left_rook is not None and left_rook.value == 500 and not left_rook.has_moved:
                #le case in mezzo (colonne 1, 2 e 3) devono essere libere
                if grid[self.row][1] is None and grid[self.row][2] is None and grid[self.row][3] is None:
                    moves.append((self.row, 2))
        
        return moves