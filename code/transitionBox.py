import pygame
from settings import *
from hitbox import HitBox
from utils import get_spawn_point_object_data


class TransitionBox(HitBox):
    def __init__(self, pos, size, groups, transition_code):
        super().__init__(pos, size, groups)
        self.transition_code = transition_code

    def get_transition_code(self):
        return self.transition_code

    def get_new_level_code(self):
        new_level_code = get_spawn_point_object_data(self.transition_code)[0]
        return new_level_code

