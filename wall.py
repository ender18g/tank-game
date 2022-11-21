import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self,screen,pos,orientation='horizontal'):
        # init our sprite:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/Retina/fenceYellow.png')
        if orientation =='vertical':
            self.image = pygame.transform.rotate(self.image,90)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        pass
    def draw(self,screen):
        screen.blit(self.image,self.rect)
