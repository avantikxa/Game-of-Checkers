import pygame
from gamesurface import *
from settings import *

class Game:
    def __init__(self, screen):
        self.active_piece = None # active piece
        self.board = Gamesurface() # Game that controls the board ???
        self.valid_moves = {} # Legal moves
        self.turn = black # Player who goes first
        self.screen = screen # Storing the screen so that it doesn't need to be contiously passed to this class
        self.selected = None

    # Reset the game state
    def reset(self):
        self.selected = None
        self.board = Gamesurface()
        self.turn = black
        self.valid_moves = {}

    # Update the board
    def update_board(self):
        self.board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row, col):
        """Select a piece from the board based on row and column, if valid piece return True, else return False"""

        if self.selected: #If piece selected
            result = self._move(row, col) #Move the selected piece to the row and col if possible (True or False)
            if not result: # If it cant move to row, col reset the selection to none and try again
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col) #Selecting a piece from the board based on row, col
        if piece != 0 and piece.color == self.turn: #If the piece exists and is of the current player
            self.selected = piece # Select the square containing a piece
            self.valid_moves = self.board.get_valid_moves(piece) #Find valid moves for that piece
            return True # Selection valid

        return False # Selection not valid

    

    def _move(self, row, col):
        piece = self.board.get_piece(row, col) # Selecting a square 
        if self.selected and piece == 0 and (row, col) in self.valid_moves: # If the selected square is empty and if it's a valid move for the piece
            self.board.move(self.selected, row, col) # Move currently selected piece to currently selected square
            skipped = self.valid_moves[(row,col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False #It cant move to that position

        return True #IF moved to that position, mark as True
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == black:
            self.turn = beige
        else:
            self.turn = black

    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, blue, (col * square_size + square_size//2, row * square_size + square_size//2), 15)

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()