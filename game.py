import pygame
from time import sleep
from background import draw_background, TILE_SIZE
import sys
from tank import Tank
from enemy_tank import EnemyTank
from random import randint, shuffle
from wall import Wall
from bar import Bar
from time import sleep

# init pygame
pygame.init()
clock = pygame.time.Clock()
num_enemies = 2
bullets_per_enemy = 3
padding = 100
shoot_interval = 500  # delay in ms
bullet_cost = 200
bullet_health = 200
bullet_max = 10 * bullet_cost

# define our grid
WINDOW_WIDTH = 10 * TILE_SIZE
WINDOW_HEIGHT = 8 * TILE_SIZE

# draw our screen with background
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

bg = draw_background((WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont(None, 24)
score = 10

# add our walls to sprite group
friendly_group = pygame.sprite.Group()
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


def make_enemies(enemy_group, num=1):
    current_num = len(enemy_group.sprites())
    # init enemy tanks
    for i in range(current_num, num_enemies):
        x_loc = randint(0+padding, WINDOW_WIDTH-padding)
        y_loc = randint(0+padding, WINDOW_HEIGHT-padding)
        theta = randint(0, 360)
        enemy_group.add(EnemyTank(x_loc, y_loc, theta))


def end_game():
    while True:
        screen.fill((200, 100, 100))
        img = font.render(f"GAME OVER - Press Spacebar", True, (230, 230, 230))
        img_rect = img.get_rect()
        img_rect.center = screen.get_rect().center
        screen.blit(img, img_rect)
        pygame.display.flip()
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    friendly_group.add(tank)
                    tank.health = 100
                    return 0


tank = Tank()
friendly_group.add(tank)
last_shot = pygame.time.get_ticks()

# make the bullet bar
bullet_bar = Bar('yellow', 1)
health_bar = Bar('red', 0)


# while loop that runs the game
while True:
    if not tank.alive():
        end_game()
        break
    # make enemies
    make_enemies(enemy_group, num_enemies)
    main_group.add(enemy_group, wall_group, friendly_group)

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
            if bullet_health >= bullet_cost:
                # fire a bullet
                print("FIRING BULLET")
                bullet_group.add(tank.shoot())
                bullet_health -= bullet_cost

    pygame.display.set_caption(f"FIDOH's Tank Game {clock.get_fps():.0f}")
    # update the background
    screen.blit(bg, bg.get_rect())
    # update bullets and draw bullets
    bullet_group.update(main_group)
    # update and draw tanks
    enemy_group.draw(screen)
    bullet_group.draw(screen)
    # fire enemy tank bullets
    if pygame.time.get_ticks() - last_shot >= shoot_interval:
        enemy_group.update(tank.rect.center)
        for enemy in pygame.sprite.Group.sprites(enemy_group):
            enemy_bullet_group.add(enemy.shoot())
        last_shot = pygame.time.get_ticks()
    # update enemy bullets
    enemy_bullet_group.update(main_group)
    enemy_bullet_group.draw(screen)

    # update our tank and check for collisions!
    friendly_group.update(wall_group, bullet_group,
                          enemy_group, enemy_bullet_group)
    friendly_group.draw(screen)

    # blit all of the wall using sprite group
    wall_group.draw(screen)
    # add in a score
    img = font.render(f"Score: {tank.score}", True, (255, 0, 0))
    score += 1
    screen.blit(img, (50, 50))
    # draw bullet bar
    bullet_health += 1
    if bullet_health > bullet_max:
        bullet_health = bullet_max
    bullet_bar.update(bullet_health/bullet_max)
    bullet_bar.draw(screen)
    health_bar.update(tank.health/100)
    health_bar.draw(screen)
    # last step to update our screen
    pygame.display.flip()
    # use the clock to slow down FPS
    clock.tick(60)
