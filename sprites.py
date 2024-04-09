import pygame
from pygame.sprite import _Group
from settings import *

class Player(pygame.sprite.Sprite):
    
    def __init__(self, *groups) -> None:
        super().__init__(*groups)

        # setup
        self.image = pygame.Surface(size= (WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        self.image.fill('red')

        # position
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction = -1
        else:
            self.direction = 0

    def update(self, dt):
        self.input()
        self.pos.x += self.direction * self.speed * dt
        self.rect.x = round(self.pos.x)



