import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], surf: pygame.Surface, groups: pygame.sprite.Group, tiled_layer: str) -> None:
        super().__init__(groups)
        self.tiled_layer = tiled_layer
        self.image = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
