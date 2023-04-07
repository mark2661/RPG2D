import pygame
from settings import *
from typing import Dict, Callable, TYPE_CHECKING, List, Union, Optional, Tuple
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
        self.vertical_button_offset: int = 0
        self.cursor_offset: int = -100
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)

    def draw(self) -> None:
        self.display_surface.fill(BLACK)
        # debug(self.buttons[0].clicked)
        if self.buttons:
            for button in self.buttons:
                button.draw()

    def draw_cursor(self) -> None:
        font: pygame.font = pygame.font.Font(MENU_FONT_TYPE, 40)
        text_surface = font.render("*", True, "#FFFFFF")
        text_rect = text_surface.get_rect(center=self.cursor_rect.center)
        self.display_surface.blit(text_surface, text_rect)

    def set_cursor_rect_center(self, rect: pygame.Rect) -> None:
        self.cursor_rect.center = (rect.midleft[0] + self.cursor_offset, rect.centery)

    def get_clicked_button(self) -> Optional[Button]:
        if self.buttons:
            for button in self.buttons:
                if button.is_cursor_on_button():
                    return button

        return None

    def get_next_vertical_button_offset(self) -> int:
        button_offset: int = self.vertical_button_offset
        self.vertical_button_offset += VERTICAL_BUTTON_OFFSET_INCREMENT_VALUE
        return button_offset

    def run(self) -> None:
        self.draw()
        if self.buttons:
            for button in self.buttons:
                if button.is_cursor_on_button():
                    self.set_cursor_rect_center(button.text_rect)
        self.draw_cursor()
