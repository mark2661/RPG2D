import sys

import pygame
from menu import Menu
from button import Button
from titleButton import TitleButton
from settings import *
from debug import debug
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from menuHandler import MenuHandler


class StartMenu(Menu):
    def __init__(self, menu_handler: "MenuHandler") -> None:
        super().__init__(menu_handler)
        self.vertical_button_offset = -50
        center_x, center_y = self.display_surface.get_width() // 2, self.display_surface.get_height() // 2
        self.buttons = [TitleButton("ADVENTURE QUEST", (center_x, center_y - 300)),
                        Button("New Game", (center_x, center_y + self.get_next_vertical_button_offset()),
                               click_function=self.start_game),
                        Button("Continue", (center_x, center_y + self.get_next_vertical_button_offset())),
                        Button("Options", (center_x, center_y + self.get_next_vertical_button_offset())),
                        Button("Quit", (center_x, center_y + self.get_next_vertical_button_offset()),
                               click_function=self.quit)]

        self.cursor_rect.center = (self.buttons[1].text_rect.midleft[0] + self.cursor_offset, self.buttons[1].text_rect.centery)

    def start_game(self) -> None:
        self.menu_handler.switch_to_level_handler()

    @staticmethod
    def quit() -> None:
        sys.exit()
