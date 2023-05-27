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
        self.user_event_id_offset = 0

        # events and timers
        self.enemy_attack_event = pygame.USEREVENT + self.get_user_event_id_offset()
        self.dead_object_garbage_collection_event = pygame.USEREVENT + self.get_user_event_id_offset()
        self.consumed_object_entity_garbage_collection_event = pygame.USEREVENT + self.get_user_event_id_offset()
        pygame.time.set_timer(self.enemy_attack_event, ENEMY_ATTACK_COOLDOWN_TIME)
        pygame.time.set_timer(self.dead_object_garbage_collection_event, DEAD_OBJECT_GARBAGE_COLLECTION_COOLDOWN_TIME)
        pygame.time.set_timer(self.consumed_object_entity_garbage_collection_event, OBJECT_ENTITY_FADE_COOLDOWN_TIME)

    def reset_level_handler(self) -> None:
        """
            This method is used to re-initialise the level handler and all the levels that the level handler handles.
            It should be called why "new game" is selected from the start menu.
        """
        self.level_handler = LevelHandler(event_handler=self)

    def get_user_event_id_offset(self) -> int:
        offset: int = self.user_event_id_offset
        self.user_event_id_offset += 1
        return offset

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

    def set_pause_menu(self) -> None:
        self.set_current_handler_to_menu_handler()
        self.current_handler.switch_menu("pause_menu")

    def resume_game(self) -> None:
        self.set_current_handler_to_level_handler()

    def leave_game_and_return_to_main_menu(self) -> None:
        # self.level_handler = LevelHandler(event_handler=self)
        self.menu_handler.switch_menu("start_menu")

    def process_events(self) -> None:
        event_function_map: Dict[object, Callable] = {
            self.level_handler: self.process_level_events,
            self.menu_handler: self.process_menu_events
        }

        event_function_map.get(self.current_handler, lambda *args: None)()
        self.display.fill("black")

    def process_level_events(self) -> None:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == self.enemy_attack_event:
                self.level_handler.enemy_attack_event()
            elif event.type == self.dead_object_garbage_collection_event:
                self.level_handler.dead_object_garbage_collection()
            elif event.type == self.consumed_object_entity_garbage_collection_event:
                self.level_handler.fade_object_entities()
            elif event.type == pygame.KEYUP and keys[pygame.K_ESCAPE]:
                self.set_pause_menu()

    def process_menu_events(self) -> None:
        left_mouse_button_clicked, center_mouse_button_clicked, right_mouse_button_clicked = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()

        def game_over_screen_active() -> bool:
            return self.menu_handler.current_menu == self.menu_handler.menus["game_over_menu"]

        def menu_button_clicked() -> None:
            button = self.menu_handler.current_menu.get_clicked_button()
            if button:
                button.on_click()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and left_mouse_button_clicked:
                menu_button_clicked()

            elif keys[pygame.K_SPACE] and game_over_screen_active():
                self.leave_game_and_return_to_main_menu()

    def run(self) -> None:
        self.current_handler.run()
