from settings import *
from entity import Entity
from typing import Optional, Union, List, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from tile import Tile
    from level import Level, YSortCameraGroup


class Enemy(Entity):
    def __init__(self, pos: tuple[float, float], asset_image_root_dir_path: str, level: "Level",
                 groups: List[Union["YSortCameraGroup", pygame.sprite.Sprite]], obstacle_sprites: pygame.sprite.Group):

        super().__init__(pos, asset_image_root_dir_path, groups, obstacle_sprites)

        # store the level object in associated with the instance
        self.level = level
        # start enemy moving upwards
        self.direction = pygame.math.Vector2(0, -1)

    # Overrides parent method
    def move(self, speed: Union[float, int]) -> None:
        current_tile: Tile = self.level.get_tile(self.rect.center)

        if current_tile:
            # moving upwards
            # BUG? for some reason check for == -1 doesn't work (even though that's the upwards direction)
            if self.direction.y == -1:
                next_tile_coords = (current_tile.rect.centerx, current_tile.rect.centery - TILE_SIZE)

            # moving downwards
            else:
                next_tile_coords = (current_tile.rect.centerx, current_tile.rect.centery + TILE_SIZE)

            # if the next tile isn't pathable reverse the y direction
            if not self.level.get_tile(next_tile_coords).is_pathable():
                self.direction.y *= -1

            # call parent method to handle actual movement logic
            super(Enemy, self).move(speed)
