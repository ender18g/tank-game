import pygame
from time import sleep
from background import draw_background, TILE_SIZE
import sys
from tank import Tank
import math
from wall import Wall

# init pygame
pygame.init()
clock = pygame.time.Clock()

# define our grid
WINDOW_WIDTH = 10 * TILE_SIZE
WINDOW_HEIGHT = 8 * TILE_SIZE

# draw our screen with background
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


bg = draw_background((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont(None, 24)
score = 1024

# make a sample wall
wall1 = Wall(screen,(300,300))
wall2 = Wall(screen,(400,400),'vertical')

# add our walls to sprite group
wall_group = pygame.sprite.Group()
wall_group.add(wall1,wall2)
# init a tank instance
tank = Tank()

# while loop that runs the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # check for keydowns
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            if event.key == pygame.K_UP:
                tank.change_speed(1)
            if event.key == pygame.K_DOWN:
                tank.change_speed(-1)
            if event.key == pygame.K_RIGHT:
                tank.change_omega(1)
            if event.key == pygame.K_LEFT:
                tank.change_omega(-1)
        if(event.type == pygame.MOUSEBUTTONDOWN):
            ## fire a bullet
            print(event)

    pygame.display.set_caption(f"FIDOH's Tank Game {clock.get_fps():.0f}")
    # update the background
    screen.blit(bg, bg.get_rect())
    tank.update(wall_group)
    tank.draw(screen)
    # blit all of the wall using sprite group
    pygame.sprite.Group.draw(wall_group,screen)
    # add in a score
    img = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(img, (20, 20))
    score += 1
    # last step to update our screen
    pygame.display.flip()
    # use the clock to slow down FPS
    clock.tick(60)
