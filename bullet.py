import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, theta, mother, color='Blue'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            f"images/Retina/bullet{color}3_outline.png")
        self.image = pygame.transform.rotate(self.image, theta+180)
        self.rect = self.image.get_rect()
        self.rect.center = (int(x), int(y))
        self.x = x
        self.y = y
        self.theta = theta
        self.speed = 5
        self.exp_time = 0
        self.exp_length = 350  # in ms
        self.exploded = False  # bullet has not exploded
        self.mother = mother

    def update(self, main_group):
        main_group = main_group.copy()
        pygame.sprite.Group.remove(main_group, self.mother)
        pygame.sprite.Group.remove(main_group, self)
        # check for bullet hitting any other sprite
        has_collided = pygame.sprite.spritecollideany(self, main_group)
        # if the bullet has already started exploding, let it finish off
        if self.exploded:
            # if you have exploded, just wait for a time interval to kill off
            if pygame.time.get_ticks() - self.exp_time > self.exp_length:
                self.kill()
        elif has_collided:
            self.explode()
        else:
            # otherwise, keep on moving in the set direction
            self.y += self.speed * math.cos(self.theta_rads())
            self.x += self.speed * math.sin(self.theta_rads())
            self.rect.center = (int(self.x), int(self.y))

    def theta_rads(self):
        # return theta in radians
        return math.pi/180 * self.theta

    def explode(self):
        # make the bullet explode if it collided with a wall
        self.image = pygame.image.load('images/Retina/explosionSmoke2.png')
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))
        self.exp_time = pygame.time.get_ticks()
        self.exploded = True
