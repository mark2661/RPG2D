import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], image_path: str, groups: list[pygame.sprite.Sprite]) -> None:
        super().__init__(groups)
        # player sprite
        self.image = pygame.image.load(image_path).convert_alpha()
        # scale image to match screen size
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)