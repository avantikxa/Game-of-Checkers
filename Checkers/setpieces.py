from settings import *

class Piece:
    # Piece outline colour
    OUTLINE = 3
    PADDING = 20

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        
        self.x, self.y = 0, 0
        self.pos() # Set x and y coordinates

    def make_king(self):
        self.king = True

    # Position of x and y (center) based on the square it is in
    def pos(self):
        self.x = square_size * self.col + square_size // 2 
        self.y = square_size * self.row + square_size // 2

    def move(self, row, col): #Updating position to moved pos
        self.row = row
        self.col = col
        self.pos() 

    # Drawing the pieces and its outline
    def draw(self, screen):
        radius = square_size//2 - self.PADDING
        pygame.draw.circle(screen, grey, (self.x, self.y), radius + self.OUTLINE) # Outline
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius) # inner circle
        if self.king: # If piece is king, draw king on it
            screen.blit(crown, (self.x - crown.get_width()//2, self.y - crown.get_height()//2))
