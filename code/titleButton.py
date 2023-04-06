import pygame
from button import Button
from settings import *
from typing import Tuple, List, TYPE_CHECKING


class TitleButton(Button):
    def __init__(self, text: str, pos: Tuple[float, float]):
        super().__init__(text, pos)

        # override font (just size)
        self.font: pygame.font.Font = pygame.font.Font(MENU_FONT_TYPE, 80)
        self.text_surf: pygame.Surface = self.font.render(text, True, "#FFFFFF")
        self.text_rect: pygame.Rect = self.text_surf.get_rect(center=pos)

    # Override parent method
    def is_cursor_on_button(self) -> bool:
        return False
