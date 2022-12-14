import pygame
import math
from bullet import Bullet


class Tank(pygame.sprite.Sprite):
    '''This is the user tank that moves around based on mouse position'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original = pygame.image.load(
            'images/Retina/tank_blue.png').convert_alpha()
        self.image = self.original
        self.rect = self.image.get_rect()
        self.x = 200
        self.y = 200
        self.theta = 0  # this is degrees
        self.speed = 2
        self.omega = 0  # angular velocity
        self.score = 0
        self.health = 100

    def move_location(self, location):
        self.rect.center = location

    def change_speed(self, delta=1):
        # stop angular movement
        self.omega = 0
        # pass in +1 to move forward, -1 to move back
        self.speed += delta
        if self.speed > 3:
            self.speed = 3

    def change_omega(self, delta=1):
        # stop linear movement
        self.speed = 0
        self.omega += delta

    def shoot(self):
        return Bullet(self.x, self.y, self.theta, self)

    def update(self, wall_group, bullet_group, enemy_group, enemy_bullet_group):
        # update the position based on speed
        theta_rads = math.pi / 180.0 * self.theta
        new_y = self.y + self.speed * math.cos(theta_rads)
        new_x = self.x + self.speed * math.sin(theta_rads)
        # new rectangle is rectangle of tank
        old_rect = self.rect
        # update x and y position of current rect
        self.rect.center = (new_x, new_y)

        # if the new position does not hit a wall, set x,y to new pos
        if (not pygame.sprite.spritecollide(self, wall_group, False)):
            self.y = new_y
            self.x = new_x
        else:
            # go back to the old rectangle
            self.rect = old_rect
            # do not update self.y and self.x
        # NEW FEATURE CHANGE ANGLE BASED ON MOUSE
        # get the mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        delta_x = mouse_x - self.x
        delta_y = self.y - mouse_y
        # find the angle to mouse and pass to tank theta
        self.theta = math.atan2(delta_y, delta_x) * 180/math.pi + 90
        # now update the rectangle position
        intX = int(self.x)
        intY = int(self.y)
        self.rect.center = (self.x, self.y)
        # twist the tank by theta
        self.image = pygame.transform.rotate(self.original, self.theta)
        # get a new rectangle for the updated/rotated image
        self.rect = self.image.get_rect(center=self.rect.center)

        # check to see if our tank killed an enemy
        self.check_offense(bullet_group, enemy_group)
        self.check_defense(enemy_bullet_group)

    def check_offense(self, bullet_group, enemy_group):
        collisions = pygame.sprite.groupcollide(
            bullet_group, enemy_group, False, True)
        if (collisions):
            for bullet in collisions:
                bullet.explode()
                self.score += 100

    def check_defense(self, enemy_bullet_group):
        collision = pygame.sprite.spritecollideany(self, enemy_bullet_group)
        if collision:
            self.health -= 1
        if self.health <= 0:
            self.kill()

    def draw(self, screen):
        # draw tank on the screen
        screen.blit(self.image, self.rect)
