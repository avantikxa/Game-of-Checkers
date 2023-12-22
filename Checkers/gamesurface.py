import pygame
from settings import *
from setpieces import *

class Gamesurface:
    def __init__(self):
        self.board = [] # draw board
        self.p1_left = self.p2_left = 12  # Number of pieces remaining with P1 and P2
        self.p1_kings = self.p2_kings = 0 #p1 = black and p2 = beige
        self.draw_pieces()

    # Moving pieces (switching old and new pieces (0 and piece))
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == rows - 1 or row == 0:
            piece.make_king() # make piece king if it reaches opp end of board
            if piece.color == beige:
                self.p2_kings += 1
            else:
                self.p1_kings += 1
    
    def get_piece(self, row, col):
        return self.board[row][col]

    def squares(self, screen):
        screen.fill(black)
        for row in range(rows):
            for col in range(row % 2, cols, 2): # Alternatively drawing colored squares
                pygame.draw.rect(screen, beige, (row*square_size, col*square_size, square_size, square_size)) #Drawing squares

    # logical drawing of pieces
    def draw_pieces(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, beige))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, black))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    # drawing pieces on screen
    def draw(self, screen):
        self.squares(screen)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == black:
                    self.p1_left -= 1
                else:
                    self.p2_left -= 1

    def evaluate(self):
        ## Evaluating board based on number of pieces left and number of pieces turned to kings
        # p1 = black and p2 = white
        return self.p2_left - self.p1_left + (self.p2_kings * 0.75 - self.p1_kings * 0.75)
    
    def get_all_pieces(self, color):
        pieces = [] # List storing all pieces of single color
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color: #Fetching all the pieces on the board of one color
                    pieces.append(piece)
        return pieces


    def winner(self):
        if self.p1_left <= 0:
            return beige
            
        elif self.p2_left <= 0:
            return black
        
        return None 

    def get_valid_moves(self, piece):
        moves = {} # Keys are positions that can be moved to whereas the values are the pieces that may be jumped while moving to that position.
        
        # Fetching diagonal pieces
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == black or piece.king:
            moves.update(self._traverse_left(row - 1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row-3, -1), -1, piece.color, right))


        if piece.color == beige or piece.king:
            moves.update(self._traverse_left(row + 1, min(row+3, rows), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row+3, rows), 1, piece.color, right))

        # print(moves)
        return moves


    #step top left or top right diagonal
    #skipped: if pcs have been skipped
    #left: col we are going to when traversing left

    #Example:
    # moves.update(self._traverse_left_pieces(row - 1, max(row-3, -1), -1, piece.color, left))
    # start = row - 1 (traversing upward); 
    # stop = max(row-3, -1) Looking 2 rows above the current row; -1 means look at row 0
    # step = -1 Moving up
    # Left is the left col

    def _traverse_left(self, start, stop, step, color, left, skipped = []):
        moves = {}
        last = [] #The pos of piece that was skipped
        for r in range(start, stop, step):           
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0: #Empty square
                if skipped and not last: # if piece was skipped and no blank square after first jump then cant jump anymore
                    break # Break turn
                elif skipped: # If skipped a piece (double jump)
                    moves[(r,left)] = last + skipped
                else: # If nothing was skipped and last existed
                    moves[(r, left)] = last
                if last: # Something was skipped and current is empty square, check if double or triple jump is possible
                    if step == -1: 
                        row = max(r-3, 0) 
                    else:
                        row = min(r+3, rows)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped = last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped = last))
                break
                    
            elif current.color == color: # If square was not empty and it's the current users color, don't allow movement
                break # No moves added

            else: #If it wasn't our color it could be moved upon if the next square is empty
                last = [current] # Store position of skipped piece
            left -= 1
        return moves

        

    def _traverse_right(self, start, stop, step, color, right, skipped = []):
        moves = {}
        last = [] #The pos of piece that was skipped
        for r in range(start, stop, step):           
            if right >= cols:
                break

            current = self.board[r][right]
            if current == 0: #Empty square
                if skipped and not last: # if piece was skipped and no blank square after first jump then cant jump anymore
                    break # Break turn
                elif skipped: # If skipped a piece (Double jump)
                    moves[(r,right)] = last + skipped
                else: # If nothing was skipped and last existed
                    moves[(r, right)] = last
                if last: # Something was skipped and current is empty square, check if double or triple jump is possible
                    if step == -1: 
                        row = max(r-3, 0) 
                    else:
                        row = min(r+3, rows)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped = last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped = last))
                break
                    
            elif current.color == color: # If square was not empty and it's the current users color, don't allow movement
                break # No moves added

            else: #If it wasn't our color it could be moved upon if the next square is empty
                last = [current] # Store position of skipped piece

            right += 1

        return moves


