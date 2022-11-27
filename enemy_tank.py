import pygame
import math
from bullet import Bullet
from random import randint


class EnemyTank(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, omega=0):
        pygame.sprite.Sprite.__init__(self)
        self.original = pygame.image.load(
            'images/Retina/tank_red.png')
        self.image = self.original
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.theta = 0  # this is degrees
        self.speed = 0
        self.omega = omega  # angular velocity
        # move to the proper location
        self.move_location((x, y))

    def move_location(self, location):
        self.rect.center = location

    def change_speed(self, delta=1):
        # stop angular movement
        self.omega = 0
        # pass in +1 to move forward, -1 to move back
        self.speed += delta

    def change_omega(self, delta=1):
        # stop linear movement
        self.speed = 0
        self.omega += delta

    def shoot(self):
        return Bullet(self.x, self.y, self.theta, self, 'Red')

    def update(self, aim_location=(0, 0)):
        # update the angle based on aim location
        delta_x = aim_location[0] - self.x
        delta_y = self.y - aim_location[1]
        # find the angle to mouse and pass to tank theta
        self.theta = math.atan2(delta_y, delta_x) * 180/math.pi + 90
        self.theta += randint(-5, 5)
        # twist the tank by theta
        self.image = pygame.transform.rotate(self.original, self.theta)
        # get a new rectangle for the updated/rotated image
        self.rect = self.image.get_rect(center=self.rect.center)
