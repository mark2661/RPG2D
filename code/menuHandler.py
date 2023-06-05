from startMenu import StartMenu
from gameOverMenu import GameOverMenu
from pauseMenu import PauseMenu
from typing import Dict, List, TYPE_CHECKING, Tuple, Callable

if TYPE_CHECKING:
    from eventHandler import EventHandler


class MenuHandler:
    """
    The MenuHandler class is responsible for managing different menus in the game.Its main purpose is to handle
    menu-related functionality and facilitate smooth transitions between different menus in the game.
    """
    def __init__(self, event_handler: "EventHandler") -> None:
        self.menus: Dict[str, StartMenu] = {
                                            "start_menu": StartMenu(menu_handler=self),
                                            "game_over_menu": GameOverMenu(menu_handler=self),
                                            "pause_menu": PauseMenu(menu_handler=self)
                                           }
        self.event_handler = event_handler
        self.current_menu = self.menus["start_menu"]
        # self.current_menu = self.menus["pause_menu"]

    def switch_menu(self, menu_code: str) -> None:
        """
           Switches the current menu based on the menu code provided, updating the current menu to the corresponding
           menu object.
        """
        if menu_code in self.menus:
            self.current_menu = self.menus[menu_code]

    def switch_to_level_handler(self) -> None:
        self.event_handler.set_current_handler_to_level_handler()

    def run(self) -> None:
        self.current_menu.run()
