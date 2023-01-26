import pygame
import sys
import os
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # create a single level for testing
        # to be removed later
        self.level = Level(os.path.join(MAPS_FILE_PATH, "0.tmx"))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.main_screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
