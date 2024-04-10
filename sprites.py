from typing import Any
import pygame
from pygame.sprite import _Group
from settings import *
from random import choice

class Player(pygame.sprite.Sprite):
    
    def __init__(self, *groups, surfacemaker) -> None:
        super().__init__(*groups)

        # setup
        self.surfacemaker = surfacemaker
        self.image = surfacemaker.get_surf(block_type= 'player', size= (WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))

        # position
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))

        # create old rect
        self.old_rect = self.rect.copy()

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
        self.old_rect = self.rect.copy()
        self.input()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        self.screen_constraint()


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, player, blocks) -> None:
        super().__init__(groups)

        # collision objects
        self.player = player
        self.blocks = blocks

        # graphics setup
        self.image = pygame.image.load('*file location').convert_alpha()

        # position setup
        self.rect = self.image.get_rect(midbottom = player.rect.midtop)
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2(x= choice((1, -1)), y= -1)
        self.speed = 400
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # active
        self.active = False

    def window_collision(self, direction):
        if direction == 'horizontal':
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1
            elif self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1

        elif direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1
            elif self.rect.bottom > WINDOW_HEIGHT:
                self.active = False
                self.direction.y = -1


    def collision(self, direction):
        # find overlapping objects
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)
        
        if overlap_sprites:
            if direction == 'horizontal':
                for sprite in overlap_sprites:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left - 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1

                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1

                    if getattr(sprite, 'health', None):
                        sprite.get_damage(1)

            elif direction == 'vertical':
                for sprite in overlap_sprites:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1

                    if getattr(sprite, 'health', None):
                        sprite.get_damage(1)


    def update(self, dt):

        if self.active:

            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            # create old rect
            self.old_rect = self.rect.copy()

            # horizontal movement + collision
            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.pos.x)
            self.collision('')
            self.window_collision('horizontal')

            # vertical movement + collision
            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.pos.y)
            self.collision('vertical')
            self.window_collision('vertical')
        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)


class Block(pygame.sprite.Sprite):

    def __init__(self, block_type, pos, groups, surfacemaker) -> None:
        super().__init__(groups)

        self.surfacemaker = surfacemaker
        self.image = self.surfacemaker.get_surf(block_type= block_type, size= (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        # damage information
        self.health = int(block_type)
    
    def get_damage(self, amount):
        self.health -= amount

        if self.health > 0:
            # update the image
            pass
        else:
            self.kill()



