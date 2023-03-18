import pygame
import os
from hitbox import HitBox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from level import Level
    from tile import Tile


class SpawnPoint(HitBox):
    def __init__(self, pos: tuple[float, float], level: "Level", groups: list[pygame.sprite.Group], spawn_point_id):
        super().__init__(pos, (1, 1), groups)
        self.pos = pos
        self.spawn_point_id = spawn_point_id
        self.level = level
        self.tile = self.level.get_tile(self.pos)

    def get_spawn_point_id(self) -> int:
        return self.spawn_point_id

    def get_associated_tile(self) -> "Tile":
        return self.tile


