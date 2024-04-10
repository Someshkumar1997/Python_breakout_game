import pygame , sys, time
from settings import *
from sprites import Player, Ball, Block, Upgrades
from surface_maker import SurfaceMaker
from random import choice

class Game:
    def __init__(self) -> None:
        
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout Game')

        # background
        self.bg = self.create_bg()

        # sprite group setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()


        # setup
        self.surfacemaker = SurfaceMaker()
        self.player = Player(self.all_sprites, self.surfacemaker)
        self.stage_setup()
        self.ball = Ball(groups= self.all_sprites, player= self.player, blocks= self.block_sprites)

        # hearts
        self.heart_surf = pygame.image.load('../graphics/other/heart.png').convert_alpha()

    def create_upgrade(self, pos):
        upgrade_type = choice(UPGRADES)
        Upgrades(pos, upgrade_type, groups= [self.all_sprites, self.upgrade_sprites])

    def create_bg(self):
        bg_original = pygame.image.load('C:/Users/Somesh Kumar Sahoo/OneDrive/Desktop/breakout game/graphics/other/bg.png').convert()
        scale_factor = WINDOW_HEIGHT / bg_original.get_height()
        scaled_width = bg_original.get_width() * scale_factor
        scaled_height = bg_original.get_height() * scale_factor
        scaled_bg = pygame.transform.scale(surface= bg_original, size= (scaled_width, scaled_height))
        return scaled_bg
    
    def stage_setup(self):

        # cycle through all rows and columns of BLOCK MAP
        for row_index, row in enumerate(BLOCK_MAP):
            for col_index, col in enumerate(row):
                if col != ' ':
                    # Find the x and y position of each blocks
                    y = TOP_OFFSET + row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    Block(col, (x,y), [self.all_sprites, self.block_sprites], self.surfacemaker, self.create_upgrade)
   

    def display_hearts(self):
        for i in range(self.player.hearts):
            x = 2 + i * (self.heart_surf.get_width() + 2)
            self.display_surface.blit(self.heart_surf, (x, 4))

    def upgrade_collision(self):
        overlap_sprites = pygame.sprite.spritecollide(self.player, self.upgrade_sprites, True)
        for sprite in overlap_sprites:
            self.player.upgrade(sprite.upgrade_type)


    def run(self):
        last_time = time.time()
        
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.player.hearts <= 0:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True


            # draw bg
            self.display_surface.blit(self.bg, (0,0))

            # update the game
            self.all_sprites.update(dt)
            self.upgrade_collision()
            
            # draw the frame
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()


            # update window
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()