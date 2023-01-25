import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], image_path: str, groups: list[pygame.sprite.Sprite],
                 obstacle_sprites: pygame.sprite.Group):
        super().__init__(groups)
        # player sprite
        self.image = pygame.image.load(image_path).convert_alpha()
        # scale image to match screen size
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 6

        # collisions
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()
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

    def move(self, speed: float):
        # normalise the direction vector so both diagonal speeds always have a magnitude of 1
        if self.direction.magnitude() != 0: self.direction = self.direction.normalize()

        # update horizontal velocity
        self.rect.x += self.direction.x * speed

        # check for horizontal collision
        self.collision("horizontal")

        # update vertical velocity
        self.rect.y += self.direction.y * speed

        # check for vertical collision
        self.collision("vertical")

    def collision(self, direction: str):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # player moving to the right
                    if self.direction.x > 0: self.rect.right = sprite.rect.left

                    # player moving to the left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # player moving to the down
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top

                    # player moving to the up
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)
