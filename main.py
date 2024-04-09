import pygame , sys, time
from settings import *
from sprites import Player, Ball, Block

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

        # setup
        self.player = Player(self.all_sprites)
        self.ball = Ball(groups= self.all_sprites, player= self.player)
        self.stage_setup()

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
                
                # Find the x and y position of each blocks
                y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                Block(col, (x,y), [self.all_sprites])
   


    def run(self):
        last_time = time.time()
        
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True


            
            # update the game
            self.all_sprites.update(dt)
            
            # draw the frame
            self.display_surface.blit(self.bg, (0,0))
            self.all_sprites.draw(self.display_surface)


            # update window
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()