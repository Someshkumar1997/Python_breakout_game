import pygame
from settings import *


class SurfaceMaker:
    # import all the graphics 
    # create one surface with the graphics with any size
    # return that image to the blocks or the player


    def get_surf(self, block_type, size):
        image = pygame.SurfaceType(size)
        image.fill('red')
        return image