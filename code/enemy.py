from settings import *
from entity import Entity
from typing import Optional
import pygame
from tile import Tile


class Enemy(Entity):
    def __init__(self, pos: tuple[float, float], asset_image_root_dir_path: str, groups: list[pygame.sprite.Sprite],
                 obstacle_sprites: pygame.sprite.Group):

        super().__init__(pos, asset_image_root_dir_path, groups, obstacle_sprites)

    def move(self, speed: float) -> None:
        # current_tile: Tile =
        # if self.direction.y == 1:

        pass

    def get_current_tile(self) -> Optional[Tile]:
