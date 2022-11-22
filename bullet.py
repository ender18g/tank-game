import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,theta):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/Retina/bulletBlue3_outline.png')
        self.image = pygame.transform.rotate(self.image,theta+180)
        self.rect = self.image.get_rect()
        self.rect.center = (int(x),int(y))
        self.x = x
        self.y = y
        self.theta = theta
        self.speed = 5
    def update(self):
        self.y += self.speed * math.cos(self.theta_rads())
        self.x += self.speed * math.sin(self.theta_rads())
        self.rect.center = (int(self.x),int(self.y))
    def theta_rads(self):
        # return theta in radians
        return math.pi/180 * self.theta
