import pygame
from settings import *
from typing import Dict, Callable, TYPE_CHECKING, List, Union, Optional
from button import Button
from titleButton import TitleButton
from debug import debug
from abc import ABC

if TYPE_CHECKING:
    from menuHandler import MenuHandler


class Menu(ABC):
    def __init__(self, menu_handler: "MenuHandler") -> None:
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.menu_handler: "MenuHandler" = menu_handler
        self.buttons: Union[Button, TitleButton] = []

    def draw(self) -> None:
        self.display_surface.fill(BLACK)
        debug(self.buttons[0].clicked)
        if self.buttons:
            for button in self.buttons:
                button.draw()

    def run(self) -> None:
        self.draw()
        if self.buttons:
            for button in self.buttons:
                if button.is_clicked():
                    button.on_click()

