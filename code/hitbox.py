import pygame
from settings import *
from typing import Tuple


class HitBox(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], size: tuple[float, float], groups: list[pygame.sprite.Group]):
        super().__init__(groups)
        self.pos = tuple(map(lambda coord: coord * SCALE, pos))
        self.size = tuple(map(lambda dimension: dimension * SCALE, size))
        self.rect = pygame.Rect(self.pos, self.size)

    def get_position(self) -> Tuple[float, float]:
        return self.pos
