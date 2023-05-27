import pygame
import os
from hitbox import HitBox
from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from level import Level
    from tile import Tile


class SpawnPoint(HitBox):
    def __init__(self, pos: Tuple[float, float], level: "Level", groups: list[pygame.sprite.Group],
                 spawn_point_id: int = None, spawn_point_type: str = None) -> None:

        super().__init__(pos, (1, 1), groups)
        self.spawn_point_id: int = spawn_point_id
        self.spawn_point_type: str = spawn_point_type
        self.level: "Level" = level

    def get_spawn_point_id(self) -> Optional[int]:
        return self.spawn_point_id

    def get_associated_tile(self) -> "Tile":
        return self.level.get_tile(self.init_pos)

    def get_spawn_point_type(self) -> Optional[str]:
        return self.spawn_point_type

    def update_level(self, new_level: "Level") -> None:
        self.level = new_level


