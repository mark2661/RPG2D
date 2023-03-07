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

    def move(self, speed: float) -> None:
        # current_tile: Tile =
        # if self.direction.y == 1:

        pass
