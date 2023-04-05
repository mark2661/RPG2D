import pygame
from settings import *
from typing import TYPE_CHECKING, Tuple, List, Dict, Callable


class Button:
    def __init__(self, text: str, pos: Tuple[float, float], width: float, height: float,
                 click_function: Callable = lambda *args: None) -> None:
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.click_function: Callable = click_function

        # top rect
        self.top_rect: pygame.Rect = pygame.Rect(pos, (width, height))
        self.top_rect.center = pos
        self.top_colour: str = "#475F77"

        # text
        self.font: pygame.font.Font = pygame.font.Font(None, 100)
        self.text_surf: pygame.Surface = self.font.render(text, True, "#FFFFFF")
        self.text_rect: pygame.Rect = self.text_surf.get_rect(center=self.top_rect.center)

        # status
        self.clicked: bool = False

    def draw(self) -> None:
        pygame.draw.rect(self.display_surface, self.top_colour, self.text_rect)
        self.display_surface.blit(self.text_surf, self.text_rect)

    def is_clicked(self) -> bool:
        mouse_pos: tuple[float, float] = pygame.mouse.get_pos()
        return self.top_rect.collidepoint(mouse_pos)

    def on_click(self) -> None:
        self.clicked = True
        self.click_function()
        self.clicked = False
