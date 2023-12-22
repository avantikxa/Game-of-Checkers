from copy import deepcopy
import pygame
from gamesurface import *
from gamelogic import *
from settings import *
# Deepcopy copies object itself
# Shallow copy copies ref to object

# alpha = max_player
# beta = game

#position = the board object. based on the current position of the board, give the best possible board after this
#depth of minimax algo: gets decremented by 1 everytime we call this (its a recursive call)


#Takes in a board/pos, depth of how far to evaluate, max_player to see if maximize or minimize, game
def minimax(position, depth, max_player, game, alpha = float('-inf'), beta = float('inf')):
    #max_player is boolean if maxing or min-ing
    #game = game object if game
    if depth == 0 or position.winner() != None: #If we're furthest down the branch or if someone has won
        return position.evaluate(), position  #gives best (max/min) number and the position it corresponds to

    if max_player: #Maximizing
        best = float('-inf') #Initial min value
        best_move = None  #No best move decided
        for move in get_all_moves(position, beige, game): #Moves related to beige
            evaluation = minimax(move, depth-1, False, game, alpha, beta)[0] # Explore next depth
            best = max(best, evaluation) #Pick the max between best and eval(last depth)
            if best == evaluation:
                best_move = move
            if best >= beta:
                return best, best_move
            if best > alpha:
                alpha = best
            

        return best, best_move
    else: # Minimizing player
        best = float('inf')
        best_move = None
        for move in get_all_moves(position, black, game):
            evaluation = minimax(move, depth-1, True, game, alpha, beta)[0]
            best = min(best, evaluation)
            if best == evaluation:
                best_move = move
            if best <= alpha:
                return best, best_move
            if best < beta:
                beta = best
            

        return best, best_move


# ALL the moves of all the pieces
def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        # (row, col) : [pieces]
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board




 