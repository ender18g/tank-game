import pygame
from time import sleep
from background import draw_background, TILE_SIZE
import sys
from tank import Tank
from enemy_tank import EnemyTank
from random import randint, shuffle
from wall import Wall

# init pygame
pygame.init()
clock = pygame.time.Clock()
num_enemies = 1
bullets_per_enemy = 3
padding = 100
shoot_delay = 150  # smaller delay for more shots
bullet_cost = 200

# define our grid
WINDOW_WIDTH = 10 * TILE_SIZE
WINDOW_HEIGHT = 8 * TILE_SIZE

# draw our screen with background
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

bg = draw_background((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont(None, 24)
score = 10

# add our walls to sprite group
wall_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
main_group = pygame.sprite.Group()

# build horizontal walls
for x in range(0, WINDOW_WIDTH, TILE_SIZE):
    for y in (0, WINDOW_HEIGHT-50):
        wall = Wall((x, y))
        # add the wall to our sprite group
        wall_group.add(wall)

# build vertical walls
for y in range(0, WINDOW_HEIGHT, TILE_SIZE):
    for x in (0, WINDOW_WIDTH-50):
        wall = Wall((x, y), 'vertical')
        # add the wall to our sprite group
        wall_group.add(wall)

# init a tank instance
tank = Tank()
# init enemy tanks
for i in range(num_enemies):
    x_loc = randint(0+padding, WINDOW_WIDTH-padding)
    y_loc = randint(0+padding, WINDOW_HEIGHT-padding)
    theta = randint(0, 360)
    enemy_group.add(EnemyTank(x_loc, y_loc, theta))


# while loop that runs the game
while True:
    # update main group
    main_group.empty()
    main_group.add(enemy_group, wall_group, tank)

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
        if (event.type == pygame.MOUSEBUTTONDOWN):
            if score > bullet_cost:
                # fire a bullet
                print("FIRING BULLET")
                bullet_group.add(tank.shoot())
                score -= bullet_cost

    pygame.display.set_caption(f"FIDOH's Tank Game {clock.get_fps():.0f}")
    # update the background
    screen.blit(bg, bg.get_rect())
    # update bullets and draw bullets
    bullet_group.update(main_group)
    bullet_group.draw(screen)
    # update and draw tanks
    tank.update(wall_group)
    tank.draw(screen)
    # update and draw enemy tanks
    enemy_group.draw(screen)
    # fire enemy tank bullets
    if pygame.time.get_ticks() % shoot_delay == 0:
        enemy_group.update(tank.rect.center)
        for enemy in pygame.sprite.Group.sprites(enemy_group):
            enemy_bullet_group.add(enemy.shoot())
    # update enemy bullets
    enemy_bullet_group.update(main_group)
    enemy_bullet_group.draw(screen)

    # blit all of the wall using sprite group
    wall_group.draw(screen)
    # add in a score
    img = font.render(f"Score: {score}", True, (255, 0, 0))
    score += 1
    screen.blit(img, (50, 50))
    # last step to update our screen
    pygame.display.flip()
    # use the clock to slow down FPS
    clock.tick(60)
