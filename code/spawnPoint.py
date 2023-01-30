import pygame
import os
from hitbox import HitBox


class SpawnPoint(HitBox):
    def __init__(self, pos: tuple[float, float], groups: list[pygame.sprite.Group], spawn_point_id):
        super().__init__(pos, (1, 1), groups)
        self.spawn_point_id = spawn_point_id

    def get_spawn_point_id(self):
        return self.spawn_point_id
