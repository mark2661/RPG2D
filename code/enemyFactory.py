import pygame
from typing import List, TYPE_CHECKING
from enemy import Enemy
from settings import *

if TYPE_CHECKING:
    from level import Level
    from spawnPoint import SpawnPoint


class EnemyFactory:
    def __init__(self):
        pass

    def create_enemy(self, enemy_spawn_point: "SpawnPoint", enemy_level: "Level") -> Enemy:
        # level_groups: List[pygame.sprite.Group] = level.get_level_groups()
        return Enemy(spawn_point=enemy_spawn_point, asset_image_root_dir_path=ENEMY_IMAGES_FILE_PATH, level=enemy_level,
                     groups=[enemy_level.visible_sprites, enemy_level.obstacle_sprites],
                     obstacle_sprites=enemy_level.obstacle_sprites)
