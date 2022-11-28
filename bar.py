import pygame


class Bar(pygame.sprite.Sprite):
    def __init__(self, color, place=0):
        super().__init__()
        self.place = place
        self.color = color
        self.colors = {'red': (230, 10, 10), 'blue': (
            53, 66, 252), 'yellow': (233, 247, 39)}
        self.update()

    def update(self, status=1):
      # make a boullet bar and fill with yellow
        self.image = pygame.Surface((50, 800))
        self.rect = self.image.get_rect()
        self.image.fill(self.colors.get(self.color))

        # take the top portion and fill in with gray
        fill_height = int((1-status) * self.rect.height)
        self.image.fill((100, 100, 100), (0, 0, 50, fill_height))
        # set alpha for transparancy
        self.rect.topleft = (50+self.place*75, 100)
        self.image.set_alpha(110)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
