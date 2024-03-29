import os
import pygame
from settings import *
from collections import defaultdict
from utils import get_spawn_point_object_data, get_spawn_point_id
from spawnPoint import SpawnPoint


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], image_path: str, groups: list[pygame.sprite.Sprite],
                 obstacle_sprites: pygame.sprite.Group):

        super().__init__(groups)
        # player sprite
        self.image = pygame.image.load(image_path).convert_alpha()
        # scale image to match screen size
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

        # general setup
        self.animations = defaultdict(lambda: [])
        self.import_assets()
        self.status = "down"  # status keeps track of the current action and direction of the player
        self.display_surface = pygame.display.get_surface()

        # attacking monitors whether or not the entity is attacking
        # attack mechanics not currently implemented
        self.attacking = False

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.frame_index = 0
        self.animation_speed = 0.15

        # collisions
        self.obstacle_sprites = obstacle_sprites

    def import_assets(self):
        for folder in os.listdir(PLAYER_IMAGES_FILE_PATH):
            folder_path = os.path.join(PLAYER_IMAGES_FILE_PATH, folder)
            for image in os.listdir(folder_path):
                image_path = os.path.join(folder_path, image)
                surf = pygame.image.load(image_path).convert_alpha()
                # scale player image up to fit map size
                surf = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
                self.animations[folder].append(surf)

    def get_status(self):
        # idle status
        if all(velocity == 0 for velocity in self.direction) and \
                all(word not in self.status for word in ["idle", "attack"]):
            self.status += "_idle"

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
        def horizontal_collision():
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # player moving to the right
                    if self.direction.x > 0: self.rect.right = sprite.rect.left

                    # player moving to the left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

        def vertical_collision():
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    # player moving to the down
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top

                    # player moving to the up
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

        collision_type_map = {"horizontal": horizontal_collision, "vertical": vertical_collision}

        collision_type_map[direction]()

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): self.frame_index = 0

        # change the current player image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
