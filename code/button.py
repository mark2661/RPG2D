import pygame
from settings import *
from typing import TYPE_CHECKING, Tuple, List, Dict, Callable


class Button:
    def __init__(self, text: str, pos: Tuple[float, float], click_function: Callable = lambda *args: None) -> None:
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.click_function: Callable = click_function

        # text
        self.font: pygame.font.Font = pygame.font.Font(MENU_FONT_TYPE, 50)
        self.text_surf: pygame.Surface = self.font.render(text, True, "#FFFFFF")
        self.text_rect: pygame.Rect = self.text_surf.get_rect(center=pos)

        # status
        self.clicked: bool = False

    def draw(self) -> None:
        # pygame.draw.rect(self.display_surface, self.top_colour, self.text_rect)
        self.display_surface.blit(self.text_surf, self.text_rect)

    def is_cursor_on_button(self) -> bool:
        mouse_pos: tuple[float, float] = pygame.mouse.get_pos()
        return self.text_rect.collidepoint(mouse_pos)

    def on_click(self) -> None:
        self.clicked = True
        self.click_function()
        self.clicked = False
