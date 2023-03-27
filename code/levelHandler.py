import pygame.display
from typing import Dict, Tuple, Optional, TYPE_CHECKING
from settings import *
from level import Level
from player import Player
from observer import Observer

if TYPE_CHECKING:
    from spawnPoint import SpawnPoint


class LevelHandler(Observer):
    def __init__(self) -> None:
        self.display_surface: pygame.Surface = pygame.display.get_surface()

        self.levels: Dict[int, Level] = {
            0: Level(os.path.join(MAPS_FILE_PATH, "0.tmx")),
            1: Level(os.path.join(MAPS_FILE_PATH, "1.tmx"))
        }  # need to automate

        # initialise current level to the starting level
        self.current_level_code: int = 0
        self.current_level: Level = self.levels[self.current_level_code]

        # get the pygame group member objects of the current level
        # define types
        self.visible_sprites_group: pygame.sprite.Group
        self.obstacle_sprites_group: pygame.sprite.Group
        self.transition_sprites_group: pygame.sprite.Group
        self.spawn_points_group: pygame.sprite.Group

        self.visible_sprites_group, self.obstacle_sprites_group, \
            self.transition_sprites_group, self.spawn_points_group = self.current_level.get_level_groups()

        # create the player instance that will be passed between levels
        # player_spawn_position: Tuple[int, int] = tuple(map(lambda x: x // 2, self.display_surface.get_size()))
        print([point for point in self.spawn_points_group if point.spawn_point_type == "player_init"])
        player_spawn_point: "SpawnPoint" = [point for point in self.spawn_points_group if point.spawn_point_type == "player_init"][0]
        self.player: Player = Player(player_spawn_point, PLAYER_IMAGES_FILE_PATH, [self.visible_sprites_group],
                                     self.obstacle_sprites_group, self.transition_sprites_group,
                                     self.spawn_points_group,
                                     self.current_level_code)

        # pass the player instance to the current level
        self.current_level.set_player(self.player)

        # call super constructor
        super().__init__(self.player)

    def transition(self) -> None:
        # if player has collided with a transition object
        # if self.current_level_code != self.player.get_current_level_code():
        def transition_map() -> None:
            # update current level code
            self.current_level_code = self.player.get_current_level_code()

            # change current level
            self.current_level = self.levels[self.current_level_code]

            # draw new map
            self.current_level.visible_sprites.regular_draw()

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
        if self.current_level_code != self.player.get_current_level_code():
            self.transition()

        # enemies check attack radius
        else:
            self.current_level.enemy_scan()

    def run(self) -> None:
        self.current_level.run()
