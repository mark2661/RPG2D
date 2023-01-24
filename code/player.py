import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], image_path: str, groups: list[pygame.sprite.Sprite]):
        super().__init__(groups)
        # player sprite
        self.image = pygame.image.load(image_path).convert_alpha()
        # scale image to match screen size
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

        # movement
        self.direction = pygame.math.Vector2()

    def input(self):
        keys= pygame.key.get_pressed()
        up, down, left, right = keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]

        if up:
            self.direction.y = -1

        elif down:
            self.direction.y = 1

        else:
            self.direction.y = 0

        if right:
            self.direction.x = 1

        elif left:
            self.direction.x = -1

        else:
            self.direction.x = 0
