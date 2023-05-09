import pygame
from typing import List, TYPE_CHECKING, Tuple
from objectEntity import ObjectEntity
from settings import *
from spawnPoint import SpawnPoint
from hitbox import HitBox

if TYPE_CHECKING:
    from level import Level
    from player import Player


class HealthObject(ObjectEntity):

    def __init__(self, position: Tuple[float, float], level: "Level") -> None:
        self.level: "Level" = level
        self.groups: List[pygame.sprite.Group] = [level.visible_sprites]
        self.obstacle_sprites: pygame.sprite.Group = level.obstacle_sprites
        asset_images_root_dir_path: str = HEALTH_POTION_IMAGES_FILE_PATH
        # self.spawn_point = SpawnPoint(pos=position, level=self.level, groups=self.groups)
        # self.spawn_point = None
        self.hit_box = HitBox(position, (TILE_SIZE, TILE_SIZE), self.groups)
        super().__init__(self.hit_box, asset_images_root_dir_path, self.groups, self.obstacle_sprites)

    def collision(self) -> None:
        player: "Player" = self.level.player
        if self.rect.colliderect(player.rect):
            self.has_object_been_used = True

    def animate(self) -> None:
        animation: List[pygame.Surface] = self.animations["health"]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): self.frame_index = 0

        # change the current player image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)
