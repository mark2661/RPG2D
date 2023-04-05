import pygame
import sys
from settings import *
from levelHandler import LevelHandler
from menuHandler import MenuHandler
from typing import Union, Dict, Tuple, Callable


class EventHandler:
    def __init__(self):
        self.level_handler: LevelHandler = LevelHandler()
        self.menu_handler: MenuHandler = MenuHandler(event_handler=self)
        self.display = pygame.display.get_surface()
        self.current_handler: Union[LevelHandler, MenuHandler] = self.menu_handler

        # events and timers
        self.enemy_attack_event = pygame.USEREVENT + 0  # Event id 24
        self.dead_object_garbage_collection_event = pygame.USEREVENT + 1  # id 25
        pygame.time.set_timer(self.enemy_attack_event, ENEMY_ATTACK_COOLDOWN_TIME)
        pygame.time.set_timer(self.dead_object_garbage_collection_event, DEAD_OBJECT_GARBAGE_COLLECTION_COOLDOWN_TIME)

    def level_handler_active(self) -> bool:
        return self.current_handler == self.level_handler

    def menu_handler_active(self) -> bool:
        return self.current_handler == self.menu_handler

    def set_current_handler_to_level_handler(self) -> None:
        self.current_handler = self.level_handler

    def set_current_handler_to_menu_handler(self) -> None:
        self.current_handler = self.menu_handler

    def process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == self.enemy_attack_event and self.level_handler_active():
                self.level_handler.enemy_attack_event()
            elif event.type == self.dead_object_garbage_collection_event and self.level_handler_active():
                self.level_handler.dead_object_garbage_collection()

        self.display.fill("black")

    def run(self) -> None:
        self.current_handler.run()
