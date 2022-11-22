import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, orientation='horizontal'):
        # init our sprite:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/Retina/fenceYellow.png')
        if orientation == 'vertical':
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        pass