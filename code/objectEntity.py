import pygame
import os
from typing import List, TYPE_CHECKING
from abstractEntity import AbstractEntity
from abc import abstractmethod
from settings import *

if TYPE_CHECKING:
    from hitbox import HitBox


class ObjectEntity(AbstractEntity):

    def __init__(self, hit_box: "HitBox", asset_images_root_dir_path: str, groups: List[pygame.sprite.Group],
                 obstacle_sprites: pygame.sprite.Group) -> None:
        super().__init__(asset_images_root_dir_path, groups, obstacle_sprites)
        # general setup
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        default_image_path: str = os.path.join(asset_images_root_dir_path, "down_idle", "down_idle_1.png")
        # default_image_path: str = os.path.join(asset_images_root_dir_path, "default_image", "red_square.png")
        self.image: pygame.Surface = pygame.image.load(default_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # scale image to match screen size
        self.rect: pygame.Rect = self.image.get_rect(center=hit_box.get_position())

        self.has_object_been_used: bool = False

    @abstractmethod
    def collision(self) -> None:
        pass

    @abstractmethod
    def animate(self) -> None:
        pass
