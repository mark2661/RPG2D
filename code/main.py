import pygame
import sys
import os
from settings import *
from levelHandler import LevelHandler


class Game:
    def __init__(self):
        pygame.init()
        self.main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level_handler = LevelHandler()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.main_screen.fill("black")
            self.level_handler.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
