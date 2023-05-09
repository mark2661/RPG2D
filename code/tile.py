import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], surf: pygame.Surface, groups: pygame.sprite.Group,
                 tiled_layer: str = "", pathable: bool = False) -> None:

        super().__init__(groups)
        self.tiled_layer: str = tiled_layer
        self.image: pygame.Surface = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.pathable: bool = pathable

    def is_pathable(self) -> bool:
        return self.pathable
