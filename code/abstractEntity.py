import pygame
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Dict, Callable, Optional, Tuple
from settings import *
from collections import defaultdict

if TYPE_CHECKING:
    from spawnPoint import SpawnPoint


class AbstractEntity(pygame.sprite.Sprite, ABC):

    def __init__(self, asset_images_root_dir_path: str, groups: List[pygame.sprite.Group],
                 obstacle_sprites: pygame.sprite.Group,
                 image_scale: Tuple[float, float] = (TILE_SIZE, TILE_SIZE)) -> None:
        super().__init__(groups)

        # animations
        self.animations: Dict[str, List[pygame.Surface]] = defaultdict(lambda: [])
        self.import_assets(asset_images_root_dir_path, image_scale)
        self.frame_index: int = 0
        self.animation_speed: float = 0.15

        # collisions
        self.obstacle_sprites: pygame.sprite.Group = obstacle_sprites

        # groups
        self.member_groups: List[pygame.sprite.Group] = groups

    def import_assets(self, root_dir: str, image_scale: Tuple[float, float]) -> None:
        for folder in os.listdir(root_dir):
            folder_path: str = os.path.join(root_dir, folder)
            for image in os.listdir(folder_path):
                image_path: str = os.path.join(folder_path, image)
                surf: pygame.Surface = pygame.image.load(image_path).convert_alpha()
                # scale player image up to fit map size
                surf = pygame.transform.scale(surf, image_scale)
                self.animations[folder].append(surf)

    # @abstractmethod
    # def reset(self, *args, **kwargs) -> None:
    #     pass
    @abstractmethod
    def animate(self) -> None:
        pass

    @abstractmethod
    def collision(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass
