import pygame
import sys
from settings import *
from levelHandler import LevelHandler
from menuHandler import MenuHandler
from typing import Union, Dict, Tuple, Callable


class EventHandler:
    def __init__(self):
        self.level_handler: LevelHandler = LevelHandler(event_handler=self)
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

    def set_game_over_screen(self) -> None:
        self.set_current_handler_to_menu_handler()
        self.current_handler.switch_menu("game_over_menu")

    def process_events(self) -> None:
        event_function_map: Dict[object, Callable] = {
            self.level_handler: self.process_level_events,
            self.menu_handler: self.process_menu_events
        }

        event_function_map.get(self.current_handler, lambda *args: None)()
        self.display.fill("black")

    def process_level_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == self.enemy_attack_event:
                self.level_handler.enemy_attack_event()
            elif event.type == self.dead_object_garbage_collection_event:
                self.level_handler.dead_object_garbage_collection()

    def process_menu_events(self) -> None:
        left_mouse_button_clicked, center_mouse_button_clicked, right_mouse_button_clicked = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        def game_over_screen_active() -> bool:
            return self.menu_handler.current_menu == self.menu_handler.menus["game_over_menu"]

        def menu_button_clicked() -> None:
            button = self.menu_handler.current_menu.get_clicked_button()
            if button:
                button.on_click()

        def leave_game_over_screen() -> None:
            self.level_handler = LevelHandler(event_handler=self)
            self.menu_handler.switch_menu("start_menu")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and left_mouse_button_clicked:
                menu_button_clicked()

            elif keys[pygame.K_SPACE] and game_over_screen_active():
                leave_game_over_screen()

    def run(self) -> None:
        self.current_handler.run()
