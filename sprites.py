from typing import Any
import pygame
from pygame.sprite import _Group
from settings import *
from random import choice

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
            self.direction.x = 0

    def screen_constraint(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.pos.x = self.rect.x
        elif self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x


    def update(self, dt):
        self.input()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        self.screen_constraint()


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, player) -> None:
        super().__init__(groups)

        # collision objects
        self.player = player

        # graphics setup
        self.image = pygame.image.load('*file location').convert_alpha()

        # position setup
        self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        self.direction = pygame.math.Vector2(x= choice((1, -1)), y= -1)
        self.speed = 400
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # active
        self.active = False
    def update(self, dt):

        if self.active:
            pass
        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)


