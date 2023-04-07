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
                        Button("Resume", (center_x, center_y + self.get_next_vertical_button_offset()),
                               click_function=self.un_pause_game),
                        Button("Options", (center_x, center_y + self.get_next_vertical_button_offset())),
                        Button("Exit to menu", (center_x, center_y + self.get_next_vertical_button_offset()),
                               click_function=self.exit_to_start_menu)]

    def un_pause_game(self) -> None:
        self.menu_handler.event_handler.resume_game()

    def exit_to_start_menu(self) -> None:
        self.menu_handler.event_handler.leave_game_and_return_to_main_menu()

    def draw_last_game_frame(self) -> None:
        player = self.menu_handler.event_handler.level_handler.current_level.player
        self.menu_handler.event_handler.level_handler.current_level.visible_sprites.custom_draw(player)

    def draw(self) -> None:
        self.draw_last_game_frame()
        self.display_surface.set_alpha(0)
        if self.buttons:
            for button in self.buttons:
                button.draw()
