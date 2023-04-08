import pygame
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Dict, Callable, Optional
from settings import *
from collections import defaultdict

if TYPE_CHECKING:
    from spawnPoint import SpawnPoint


class AbstractEntity(pygame.sprite.Sprite, ABC):

    def __init__(self, spawn_point: "SpawnPoint", asset_images_root_dir_path: str, groups: List[pygame.sprite.Group],
                 obstacle_sprites: pygame.sprite.Group) -> None:
        super().__init__(groups)

        # general setup
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        default_image_path: str = os.path.join(asset_images_root_dir_path, "down_idle", "down_idle_1.png")
        self.spawn_point: "SpawnPoint" = spawn_point
        self.image: pygame.Surface = pygame.image.load(default_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # scale image to match screen size
        self.rect: pygame.Rect = self.image.get_rect(topleft=self.spawn_point.get_associated_tile().rect.topleft)

        # animations
        self.animations: Dict[str, List[pygame.Surface]] = defaultdict(lambda: [])
        self.import_assets(asset_images_root_dir_path)

        # collisions
        self.obstacle_sprites: pygame.sprite.Group = obstacle_sprites

        # groups
        self.member_groups: List[pygame.sprite.Group] = groups

    def import_assets(self, root_dir: str) -> None:
        for folder in os.listdir(root_dir):
            folder_path: str = os.path.join(root_dir, folder)
            for image in os.listdir(folder_path):
                image_path: str = os.path.join(folder_path, image)
                surf: pygame.Surface = pygame.image.load(image_path).convert_alpha()
                # scale player image up to fit map size
                surf = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
                self.animations[folder].append(surf)

    @abstractmethod
    def animate(self) -> None:
        pass

    @abstractmethod
    def collision(self) -> None:
        pass
