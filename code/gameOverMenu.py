from menu import Menu
from typing import TYPE_CHECKING
from button import Button
from titleButton import TitleButton

if TYPE_CHECKING:
    from menuHandler import MenuHandler


class GameOverMenu(Menu):
    def __init__(self, menu_handler: "MenuHandler") -> None:
        super().__init__(menu_handler)
        center_x, center_y = self.display_surface.get_width() // 2, self.display_surface.get_height() // 2
        self.buttons = [TitleButton("Game Over", (center_x, center_y - 200)),
                        Button("Press Space to Continue", (center_x, center_y))]
        self.cursor_rect.center = (
            self.buttons[1].text_rect.midleft[0] + self.cursor_offset, self.buttons[1].text_rect.centery)

    # Override parent method
    def draw_cursor(self) -> None:
        return
