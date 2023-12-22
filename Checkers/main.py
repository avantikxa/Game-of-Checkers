import pygame
import sys
from settings import *
from gamesurface import *
from gamelogic import *
from minmax import *
import timeit


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Checkers')


# Grab row and column that user is in based on mouse position
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // square_size
    col = x // square_size
    return row, col

def main():
    singlePlayer = True
    play = True

    game = Game(screen)


    while play: 
        for event in  pygame.event.get():

            if singlePlayer:
                if game.turn == beige: #AI's turn
                    #value is score attached to state 
                    value, new_board = minimax(game.get_board(),4, beige, game) #depth 4 = fast, 5 = works, 6 = pushing it, 6+ broken
                    # start = timeit.default_timer()
                    game.ai_move(new_board) #AI has moved so update the board to new board
                    # end = timeit.default_timer()
                    # total = end - start
                    # print(f"Time taken for AI Move {total*10**3:.03f}")

            if event.type == pygame.QUIT:
                play = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: # Mouse is clicked
                pos = pygame.mouse.get_pos() #Grab mouse position
                row, col = get_row_col_from_mouse(pos) # Find row and column that user is in based on mouse pos
                game.select(row,col)

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: #Press Q to quit
                    play = False

        game.update_board()
        
    pygame.quit()

main()

            



