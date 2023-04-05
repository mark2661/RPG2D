import pygame
import sys
from settings import *
from eventHandler import EventHandler


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.main_screen: pygame.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.event_handler: EventHandler = EventHandler()
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def run(self) -> None:
        while True:
            self.event_handler.process_events()
            self.event_handler.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game: Game = Game()
    game.run()
