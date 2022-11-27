import pygame


class Bar(pygame.sprite.Sprite):
    def __init__(self, color="yellow", place=0):
        super().__init__()
        self.place = place
        self.color = color
        self.update()

    def update(self, status=1):
      # make a boullet bar and fill with yellow
        self.image = pygame.Surface((50, 800))
        self.rect = self.image.get_rect()
        if self.color == 'red':
            self.image.fill((200, 0, 0))
        else:
            self.image.fill((235, 222, 52))

        # take the top portion and fill in with gray
        fill_height = int((1-status) * self.rect.height)
        self.image.fill((100, 100, 100), (0, 0, 50, fill_height))
        # set alpha for transparancy
        self.rect.topleft = (50+self.place*75, 100)
        self.image.set_alpha(150)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
