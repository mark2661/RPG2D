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

    def __init__(self, position: Tuple[float, float], level: "Level", health: int = 0) -> None:
        self.level: "Level" = level
        self.groups: List[pygame.sprite.Group] = [self.level.visible_sprites]
        self.obstacle_sprites: pygame.sprite.Group = self.level.obstacle_sprites
        asset_images_root_dir_path: str = HEALTH_POTION_IMAGES_FILE_PATH
        self.hit_box = HitBox(position, (TILE_SIZE, TILE_SIZE), self.groups)
        super().__init__(self.hit_box, asset_images_root_dir_path, self.groups, self.obstacle_sprites)
        self.animation_speed = 0.075

    def reset(self, new_level: "Level") -> None:
        self.level = new_level

        def reset_transparency() -> None:
            animations: List[pygame.Surface] = self.animations["health"]
            for animation in animations:
                animation.set_alpha(255)

        def reset_level_groups() -> None:
            # ensure sprite is removed from all previous groups
            self.kill()
            # add sprite group to the new levels pygame.sprite.Sprite.groups instance var
            self.add(self.level.visible_sprites)

            # self.hit_box.kill()
            # self.hit_box.add(new_level.visible_sprites)
            self.obstacle_sprites = self.level.obstacle_sprites

        def reset_attributes() -> None:
            self.has_object_been_used = False
            # TO-DO: reset health attribute

        reset_transparency()
        reset_level_groups()
        reset_attributes()

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

    # Overrides parent method
    def update(self) -> None:
        self.collision()
        self.animate()
