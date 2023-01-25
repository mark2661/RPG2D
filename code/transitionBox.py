import pygame
from settings import *


class TransitionBox(pygame.sprite.Sprite):
    def __init__(self, pos, size, transition_code, transition_spawn_point, groups):
        super().__init__(groups)
        self.pos = tuple(map(lambda coord: coord * SCALE, pos))
        self.transition_code = transition_code
        self.transition_spawn_point = transition_spawn_point
        self.size= tuple(map(lambda dimension: dimension * SCALE, size))
        self.rect = pygame.Rect(self.pos, self.size)