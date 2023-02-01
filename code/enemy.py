from settings import *
from entity import Entity
import pygame


class Enemy(Entity):
    def __init__(self, pos: tuple[float,float], asset_image_root_dir_path: str, groups: list[pygame.sprite.Sprite],
                 obstacle_sprites: pygame.sprite.Group):

        super().__init__(pos, asset_image_root_dir_path, groups, obstacle_sprites)