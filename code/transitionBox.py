import pygame
from settings import *
from hitbox import HitBox


class TransitionBox(HitBox):
    def __init__(self, pos, size, groups, transition_code, transition_spawn_point):
        super().__init__(pos, size, groups)
        self.transition_code = transition_code
        self.transition_spawn_point = transition_spawn_point
