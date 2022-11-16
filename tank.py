import pygame
from pygame.sprite import Sprite
import math

class Tank(Sprite):
    def __init__(self,screen):
        self.image = pygame.image.load('images/Retina/tank_blue.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.x = 200
        self.y = 200
        self.theta = 0 # this is degrees
        self.speed = 0
        self.omega = 0 # angular velocity
        self.screen = screen

    def move_location(self,location):
        self.rect.center = location

    def change_speed(self, delta = 1 ):
        # stop angular movement
        self.omega = 0;
        # pass in +1 to move forward, -1 to move back
        self.speed+=delta

    def change_omega(self,delta =1):
        # stop linear movement
        self.speed= 0
        self.omega+=delta

    def update(self):
        # update the position based on speed
        # convert theta to radians
        theta_rads = math.pi/ 180.0 * self.theta
        self.y += self.speed * math.cos(theta_rads)
        self.x += self.speed * math.sin(theta_rads)
        # change angle
        self.theta -= self.omega


    def draw(self):
        # update location
        self.update()
        # now update the rectangle position
        intX = int(self.x)
        intY = int(self.y)
        self.rect.center = (self.x, self.y)

        # twist the tank by theta       
        rot_tank = pygame.transform.rotate(self.image, self.theta)
        # get a new rectangle for the updated/rotatd image
        rot_rect = rot_tank.get_rect(center = self.rect.center)

        self.screen.blit(rot_tank, rot_rect)
