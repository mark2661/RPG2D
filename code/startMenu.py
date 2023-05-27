import sys

import pygame
from menu import Menu
from button import Button
from titleButton import TitleButton
from settings import *
from debug import debug
from typing import TYPE_CHECKING, Callable
from objectPoolHandler import ObjectPoolHandler

if TYPE_CHECKING:
    from menuHandler import MenuHandler
    from levelHandler import LevelHandler


class StartMenu(Menu):
    def __init__(self, menu_handler: "MenuHandler") -> None:
        super().__init__(menu_handler)
        self.menu_handler: "MenuHandler" = menu_handler
        self.vertical_button_offset = -50
        center_x, center_y = self.display_surface.get_width() // 2, self.display_surface.get_height() // 2
        self.buttons = [TitleButton("ADVENTURE QUEST", (center_x, center_y - 300)),
                        Button("New Game", (center_x, center_y + self.get_next_vertical_button_offset()),
                               click_function=self.start_game()),
                        Button("Continue", (center_x, center_y + self.get_next_vertical_button_offset())),
                        Button("Options", (center_x, center_y + self.get_next_vertical_button_offset())),
                        Button("Quit", (center_x, center_y + self.get_next_vertical_button_offset()),
                               click_function=self.quit)]

        self.cursor_rect.center = (
                                   self.buttons[1].text_rect.midleft[0] + self.cursor_offset,
                                   self.buttons[1].text_rect.centery
                                  )

    def start_game(self) -> Callable:
        first_call = True

        def new_game() -> None:
            # print("new game")
            nonlocal first_call
            # print(f"first call: {first_call}")
            if not first_call:
                object_pool_handler: ObjectPoolHandler = ObjectPoolHandler()
                object_pool_handler.free_all_objects_in_all_object_pools()
                self.menu_handler.event_handler.reset_level_handler()
                level_handler: "LevelHandler" = self.menu_handler.event_handler.level_handler
                # print(f"after reset: {level_handler.levels}")
            self.menu_handler.switch_to_level_handler()
            first_call = False

        return new_game

    @staticmethod
    def quit() -> None:
        sys.exit()
