import pygame



# Constant colours
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
beige = (207, 185, 151)
grey = (128, 128, 128)

crown = pygame.transform.scale(pygame.image.load('assets/crown.png'),(50,30))


width, height = 800, 800
rows, cols = 8, 8
square_size = width//cols # How big each square is

