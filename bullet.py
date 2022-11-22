import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, theta):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 5))
        pygame.Surface.fill(self.image, (0, 0, 0))
        self.image = pygame.transform.rotate(self.image, theta)
        self.rect = self.image.get_rect()
        self.theta = theta
        self.x = x
        self.y = y
        self.speed = 5

    def update(self):
        self.x += self.speed * math.cos(self.rad_theta())
        self.y -= self.speed * math.sin(self.rad_theta())
        #print(f"{self.x} - {self.y}")
        self.rect.center = (int(self.x), int(self.y))

    def rad_theta(self):
        return math.pi/180 * self.theta
