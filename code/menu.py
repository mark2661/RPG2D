import pygame
from settings import *
from typing import Dict, Callable, TYPE_CHECKING, List
from button import Button
from debug import debug

if TYPE_CHECKING:
    from menuHandler import MenuHandler


class Menu:
    def __init__(self, menu_handler: "MenuHandler") -> None:
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.menu_handler: "MenuHandler" = menu_handler
        center_x, center_y = self.display_surface.get_width()//2, self.display_surface.get_height()//2
        self.buttons = [Button("click me", (center_x, center_y), 600, 120, click_function=self.start_game)]

    def draw(self) -> None:
        self.display_surface.fill(BLACK)
        debug(self.buttons[0].clicked)
        for button in self.buttons:
            button.draw()

    def start_game(self) -> None:
        self.menu_handler.switch_to_level_handler()

    def run(self) -> None:
        self.draw()
        for button in self.buttons:
            if button.is_clicked():
                button.on_click()

