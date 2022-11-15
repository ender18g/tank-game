import pygame
from time import sleep
from helper import grid
import sys
from tank import Tank

# init pygame
pygame.init()
clock = pygame.time.Clock()

# define our grid
TILE_SIZE = 64
WINDOW_WIDTH = 10 * TILE_SIZE
WINDOW_HEIGHT = 8 * TILE_SIZE 

# define images for our background
grass = pygame.image.load("images/Environment/grass.png")
dirt = pygame.image.load("images/Environment/dirt.png")
sand = pygame.image.load("images/Environment/sand.png")

soils = [grass,dirt,sand]

# grab the dimension of our tile rectangle
tile_rect = grass.get_rect()

# draw our screen with background
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

def draw_background():
    # draw each tile onto our background
    for r, grid_list in enumerate(grid):
        for c, grid_element in enumerate(grid_list):
            # blit the correc tile onto our screen
            screen.blit(soils[grid_element], (c*TILE_SIZE, r*TILE_SIZE))

tank = Tank(screen)


font = pygame.font.SysFont(None, 24)
score = 1024

# while loop that runs the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #check for keydowns
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
        if event.type == pygame.MOUSEMOTION:
            # use  event.pos to aim the tank
            tank.move(event.pos)

    # use the clock to slow down FPS
    clock.tick(60)
    pygame.display.set_caption(f"FIDOH's Tank Game {clock.get_fps():.0f}")
    # update the background
    draw_background()
    tank.draw()
    # add in a score
    img = font.render(f"Score: {score}", True, (255,0,0))
    screen.blit(img, (20, 20))
    score +=1

    # last step to update our screen
    pygame.display.flip()


