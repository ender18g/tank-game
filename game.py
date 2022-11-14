import pygame
from time import sleep

# init pygame
pygame.init()

# define our grid
TILE_SIZE = 64
WINDOW_WIDTH = 10 * TILE_SIZE
WINDOW_HEIGHT = 8 * TILE_SIZE 

# 0 is grass, 1 is dirt 2 is sand
grid = [
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
    [0, 0, 1, 1, 2, 2, 1, 1, 0, 0, ],
]
# define images for our background
grass = pygame.image.load("images/Environment/grass.png")
dirt = pygame.image.load("images/Environment/dirt.png")
sand = pygame.image.load("images/Environment/sand.png")

soils = [grass,dirt,sand]

# grab the dimension of our tile rectangle
tile_rect = grass.get_rect()

# draw our screen with background
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

w_loc = 0
h_loc = 0

# draw each tile onto our background
for row in grid:
    for i in row:
        # blit the correc tile onto our screen
        screen.blit(soils[i], (w_loc, h_loc))
        w_loc += TILE_SIZE
    h_loc += TILE_SIZE
    w_loc = 0



pygame.display.flip()
sleep(5)