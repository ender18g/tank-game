import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos, orientation='horizontal'):
        # init our sprite:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/Retina/fenceYellow.png')
        # assume wall is horizontal unless set to vertical
        if orientation == 'vertical':
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)
