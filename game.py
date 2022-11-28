import pygame
from time import sleep
from background import draw_background, TILE_SIZE
import sys
from tank import Tank
from enemy_tank import EnemyTank
from random import randint, choice
from wall import Wall
from bar import Bar
from time import sleep


class Game():
    def __init__(self):
        # init pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.padding = 100
        self.shoot_interval = 2000  # delay in ms
        self.bullet_cost = 200
        self.bullet_max = 10 * self.bullet_cost
        self.bullet_health = self.bullet_max
        self.num_extra_walls = 7
        # define our grid
        self.TILE_SIZE = TILE_SIZE
        self.WINDOW_WIDTH = 10 * self.TILE_SIZE
        self.WINDOW_HEIGHT = 8 * self.TILE_SIZE
        self.WINDOW_SIZE = (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        # draw our screen with background
        self.screen = pygame.display.set_mode(
            self.WINDOW_SIZE)
        self.bg = draw_background(self.WINDOW_SIZE)
        # set the font for score and messages
        self.font = pygame.font.SysFont(None, 24)

        # make all of our groups
        self.friendly_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.main_group = pygame.sprite.Group()
        self.all_bullets = pygame.sprite.Group()

        # make the friendly tank
        self.tank = Tank()
        self.friendly_group.add(self.tank)
        self.last_shot = pygame.time.get_ticks()
        # make the bullet bar and health bars
        self.bullet_bar = Bar('yellow', 1)
        self.health_bar = Bar('blue', 0)

        # setup the walls
        self.setup_map()

    def get_random_position(self):
        '''Makes a random position tuple (x,y)'''
        x_loc = randint(0+self.padding, self.WINDOW_WIDTH-self.padding)
        y_loc = randint(0+self.padding, self.WINDOW_HEIGHT-self.padding)
        return (x_loc, y_loc)

    def setup_map(self):
        # build horizontal walls
        for x in range(0, self.WINDOW_WIDTH, self.TILE_SIZE):
            for y in (0, self.WINDOW_HEIGHT-50):
                wall = Wall((x, y))
                # add the wall to our sprite group
                self.wall_group.add(wall)
        # build vertical walls
        for y in range(0, self.WINDOW_HEIGHT, self.TILE_SIZE):
            for x in (0, self.WINDOW_WIDTH-50):
                wall = Wall((x, y), 'vertical')
                # add the wall to our sprite group
                self.wall_group.add(wall)
        # build random walls
        for i in range(self.num_extra_walls):
            self.wall_group.add(Wall(self.get_random_position(),
                                choice(['vertical', 'horizontal'])))

    def make_enemies(self, num_enemies=1):
        current_num = len(self.enemy_group.sprites())
        # init enemy tanks
        for i in range(current_num, num_enemies):
            theta = randint(0, 360)
            new_enemy = EnemyTank(*self.get_random_position(), theta)
            if not pygame.sprite.spritecollideany(new_enemy, self.wall_group):
                self.enemy_group.add(new_enemy)

    def end_game(self):
        '''Ends the game and displays score / reset info'''
        while True:
            self.screen.fill((200, 100, 100))
            img = self.font.render(
                f"GAME OVER - Press Spacebar", True, (230, 230, 230))
            img_rect = img.get_rect()
            img_rect.center = self.screen.get_rect().center
            self.screen.blit(img, img_rect)
            img = self.font.render(
                f"Score: {self.tank.score}", True, (20, 20, 20))
            img_rect = img.get_rect()
            img_rect.midbottom = self.screen.get_rect().midbottom
            # draw text on screen
            self.screen.blit(img, img_rect)
            pygame.display.flip()
            self.clock.tick()
            # listen for events to reset the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        self.friendly_group.add(self.tank)
                        # reset health and score of tank
                        self.tank.health = 100
                        self.tank.score = 0
                        for sprite in self.enemy_group:
                            sprite.kill()
                        return 0

    def draw_components(self):
        pygame.display.set_caption(
            f"FIDOH's Tank Game {self.clock.get_fps():.0f}")
        # draw the background
        self.screen.blit(self.bg, self.bg.get_rect())
        # update and draw ALL sprites
        self.main_group.draw(self.screen)
        self.all_bullets.draw(self.screen)
        # add in a score
        img = self.font.render(f"Score: {self.tank.score}", True, (255, 0, 0))
        self.screen.blit(img, (50, 50))
        self.bullet_bar.draw(self.screen)
        self.health_bar.draw(self.screen)

    def update_components(self):
        # fire enemy tank bullets
        if pygame.time.get_ticks() - self.last_shot >= self.shoot_interval:
            self.enemy_group.update(self.tank.rect.center)
            for enemy in pygame.sprite.Group.sprites(self.enemy_group):
                self.enemy_bullet_group.add(enemy.shoot())
            self.last_shot = pygame.time.get_ticks()
        # update enemy bullets
        self.enemy_bullet_group.update(self.main_group)
        # update friendly bullets
        self.bullet_group.update(self.main_group)
        self.health_bar.update(self.tank.health/100)
        self.bullet_bar.update(self.bullet_health/self.bullet_max)
        # update our tank and check for collisions!
        self.friendly_group.update(self.wall_group, self.bullet_group,
                                   self.enemy_group, self.enemy_bullet_group)

    def update_calculations(self):
      # these calculations are run every iteration
        self.bullet_health += 1
        if self.bullet_health > self.bullet_max:
            self.bullet_health = self.bullet_max

    def listen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # check for keydowns
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_UP:
                    self.tank.change_speed(1)
                if event.key == pygame.K_DOWN:
                    self.tank.change_speed(-1)
                if event.key == pygame.K_RIGHT:
                    self.tank.change_omega(1)
                if event.key == pygame.K_LEFT:
                    self.tank.change_omega(-1)
            if (event.type == pygame.MOUSEBUTTONDOWN):
              # on left mouse click fire a bullet if bullets remain
                if self.bullet_health >= self.bullet_cost:
                    # fire a bullet
                    self.bullet_group.add(self.tank.shoot())
                    self.bullet_health -= self.bullet_cost

    def run_game(self):
        # while loop that runs the game
        while True:
            if not self.tank.alive():
                self.end_game()
            # make enemies
            self.make_enemies(self.tank.score//500+1)
            # add everything to main group and all bullet group
            self.main_group.add(
                self.enemy_group, self.wall_group, self.friendly_group)
            self.all_bullets.add(self.bullet_group, self.enemy_bullet_group)
            # listen for keyboard events
            self.listen_events()
            # update calculations
            self.update_calculations()
            # update components
            self.update_components()
            # draw everything
            self.draw_components()
            # last step to update our screen
            pygame.display.flip()
            # use the clock to slow down FPS
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run_game()
