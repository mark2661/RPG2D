import pygame
from pytmx.util_pygame import load_pygame
from settings import *

class Level:
    def __init__(self, map_path: str) -> None:
        # load map
        self.tmx_data = load_pygame(map_path)

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()


    def run(self):
        pass