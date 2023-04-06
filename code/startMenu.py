import pygame
from menu import Menu
from button import Button
from titleButton import TitleButton
from settings import *
from debug import debug


class StartMenu(Menu):
    def __init__(self, menu_handler: "MenuHandler") -> None:
        super().__init__(menu_handler)
        center_x, center_y = self.display_surface.get_width() // 2, self.display_surface.get_height() // 2
        self.buttons = [TitleButton("ADVENTURE QUEST", (center_x, center_y - 300)),
                        Button("New Game", (center_x, center_y), click_function=self.start_game),
                        Button("Load Game", (center_x, center_y + 100)),
                        Button("Options", (center_x, center_y + 200)),
                        Button("Quit", (center_x, center_y + 300))]

    def start_game(self) -> None:
        self.menu_handler.switch_to_level_handler()
