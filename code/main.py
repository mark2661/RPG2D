import pygame
import sys
from settings import *
from levelHandler import LevelHandler


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.main_screen: pygame.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.level_handler: LevelHandler = LevelHandler()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.main_screen.fill("black")
            self.level_handler.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game: Game = Game()
    game.run()
