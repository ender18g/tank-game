import pygame
from pygame.sprite import Sprite

class Tank(Sprite):
    def __init__(self,screen):
        self.image = pygame.image.load('images/Tanks/tankBlue_outline.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.screen = screen
        self.h_border = self.screen.get_rect().centery
        print(self.h_border)
        print(self.screen.get_rect())

    def move(self,location):
        # get the x and y of passed location
        loc_x, loc_y = location
        # added feature, tank can't go beyond halfway point
        if loc_y + self.rect.height//2 > self.h_border:
            # border is violated, stop tank at border
            self.rect.center = (loc_x,self.h_border-self.rect.height//2)
        # move our rectangle to the passed in location
        else:
            self.rect.center = location

    def draw(self):
        self.screen.blit(self.image,self.rect)
