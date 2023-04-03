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

        self.enemy_attack_event = pygame.USEREVENT + 0  # Event id 24
        self.dead_object_garbage_collection_event = pygame.USEREVENT + 1  # id 25
        pygame.time.set_timer(self.enemy_attack_event, ENEMY_ATTACK_COOLDOWN_TIME)
        pygame.time.set_timer(self.dead_object_garbage_collection_event, DEAD_OBJECT_GARBAGE_COLLECTION_COOLDOWN_TIME)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == self.enemy_attack_event:
                    self.level_handler.enemy_attack_event()
                elif event.type == self.dead_object_garbage_collection_event:
                    self.level_handler.dead_object_garbage_collection()

            self.main_screen.fill("black")
            self.level_handler.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game: Game = Game()
    game.run()
