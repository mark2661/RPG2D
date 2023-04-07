from typing import TYPE_CHECKING
from titleButton import TitleButton
from button import Button
from menu import Menu
from settings import *

if TYPE_CHECKING:
    from menuHandler import MenuHandler


class PauseMenu(Menu):
    def __init__(self, menu_handler: "MenuHandler") -> None:
        super().__init__(menu_handler)
        center_x, center_y = self.display_surface.get_width() // 2, self.display_surface.get_height() // 2
        self.buttons = [TitleButton("Paused", (center_x, center_y - 200)),
                        Button("Resume", (center_x, center_y), click_function=self.un_pause_game)]

    def un_pause_game(self) -> None:
        self.menu_handler.event_handler.resume_game()

    def draw(self) -> None:
        # self.display_surface.fill(BLACK)
        self.display_surface.set_alpha(0)
        # debug(self.buttons[0].clicked)
        if self.buttons:
            for button in self.buttons:
                button.draw()
