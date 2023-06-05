import pygame.display
from typing import Dict, Tuple, Optional, TYPE_CHECKING, Union, Callable
from settings import *
from level import Level
from player import Player
from observer import Observer
from menu import Menu
from collections import defaultdict

if TYPE_CHECKING:
    from spawnPoint import SpawnPoint
    from eventHandler import EventHandler


class LevelHandler(Observer):
    """
       The LevelHandler class manages game levels, loosely following the facade design pattern.
       It initializes the current level, handles level transitions, updates player attributes and positions when
       transitioning, and manages various game events such as enemy attacks and dead object cleanup.
    """
    def __init__(self, event_handler: "EventHandler") -> None:
        self.event_handler: "EventHandler" = event_handler
        self.display_surface: pygame.Surface = pygame.display.get_surface()

        # Hash map to store Level objects {level_code: Level}
        self.levels: Dict[int, Optional[Level]] = defaultdict(lambda: None)

        # initialise current level to the starting level
        self.current_level_code: int
        self.current_level: Level

        # get the pygame group member objects of the current level
        self.visible_sprites_group: pygame.sprite.Group
        self.obstacle_sprites_group: pygame.sprite.Group
        self.transition_sprites_group: pygame.sprite.Group
        self.spawn_points_group: pygame.sprite.Group

        self.player: Player

        self.start_game()
        # call super constructor
        super().__init__(self.player)

    def get_level(self, level_code: int) -> "Level":
        """
           Retrieves a specific level based on the given level code. If the level is not already loaded,
           it loads it from a file and caches it for future use.
        """
        if level_code not in self.levels:
            try:
                self.levels[level_code] = Level(map_path=os.path.join(MAPS_FILE_PATH, f"{level_code}.tmx"),
                                                level_handler=self)
            except IOError:
                file_path: str = os.path.join(MAPS_FILE_PATH, f"{level_code}.tmx")
                raise Exception(f"Error file: {file_path} does not exist")

        return self.levels[level_code]

    def init_player(self) -> None:
        """
            Initializes the player character by creating a Player instance and assigning it to the current level.
            It also sets up the player's sprite groups and spawn point.
        """

        self.visible_sprites_group, self.obstacle_sprites_group, \
            self.transition_sprites_group, self.spawn_points_group = self.levels[0].get_level_groups()

        # create the player instance that will be passed between levels
        player_spawn_point: "SpawnPoint" = \
            [point for point in self.spawn_points_group if point.spawn_point_type == "player_init"][0]
        self.player = Player(player_spawn_point, PLAYER_IMAGES_FILE_PATH,
                             [self.visible_sprites_group, self.obstacle_sprites_group],
                             self.obstacle_sprites_group, self.transition_sprites_group,
                             self.spawn_points_group,
                             self.current_level_code)

    def start_game(self) -> None:
        # initialise current level to the starting level
        self.current_level_code = 0
        self.current_level: Level = self.get_level(self.current_level_code)

        # pass the player instance to the current level
        self.init_player()
        self.current_level.set_player(self.player)

    def transition(self) -> None:
        """
           Handles level transitions when the player collides with a transition object.
           It updates the current level instance attribute, player attributes and position according to the
           new level (i.e. groups and spawn point).
        """
        # if player has collided with a transition object
        def transition_map() -> None:
            # update current level code
            self.current_level_code = self.player.get_current_level_code()

            # change current level
            self.current_level = self.get_level(self.current_level_code)

        def update_player_attributes() -> None:
            # update group attributes
            self.update_groups()

            # move player instance to new level
            self.current_level.set_player(self.player)

            # update player object groups
            self.player.set_groups(self.current_level.get_level_groups())

            # set new player pos
            self.player.rect.center = self.get_spawn_point(self.player.next_level_spawn_id).rect.center

        transition_map()
        update_player_attributes()

    def update_groups(self) -> None:
        # get the pygame group member objects of the current level
        self.visible_sprites_group, self.obstacle_sprites_group, \
            self.transition_sprites_group, self.spawn_points_group = self.current_level.get_level_groups()

    def get_spawn_point(self, spawn_point_id: int) -> Optional[pygame.sprite.Sprite]:
        for sprite in self.spawn_points_group:
            if sprite.get_spawn_point_id() == spawn_point_id:
                return sprite

        return None

    # Overrides parent method
    def observer_update(self) -> None:
        """
            Overrides the parent method to handle observer updates. Checks if the player has transitioned to a new
            level and triggers the transition if needed. Otherwise, it instructs Enemy objects in the current level to
            scan for the player object.
        """

        if self.current_level_code != self.player.get_current_level_code():
            self.transition()

        # enemies check attack radius
        else:
            self.current_level.enemy_scan()

    def enemy_attack_event(self) -> None:
        self.current_level.make_eligible_enemies_attack_player()

    def dead_object_garbage_collection(self) -> None:
        """
           Releases "dead" entities to their respective object pool. By instructing the current level to
           despawn dead entities.
        """
        self.current_level.de_spawn_dead_entities()

    def fade_object_entities(self) -> None:
        """
           Initiates fading of consumed object entities by instructing the current level to fade them.
        """
        self.current_level.fade_consumed_object_entities()

    def run(self) -> None:
        self.current_level.run()
