import os
import pygame
from settings import *
from collections import defaultdict
from typing import List, Dict, Callable
from utils import get_spawn_point_object_data, get_spawn_point_id
from spawnPoint import SpawnPoint


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], asset_images_root_dir_path: str, groups: List[pygame.sprite.Group],
                 obstacle_sprites: pygame.sprite.Group):

        super().__init__(groups)
        # general setup
        default_image_path = os.path.join(asset_images_root_dir_path, "down_idle", "down_idle_1.png")
        self.image = pygame.image.load(default_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # scale image to match screen size
        self.rect = self.image.get_rect(topleft=pos)

        self.animations = defaultdict(lambda: [])
        self.import_assets(asset_images_root_dir_path)
        self.status = "down"  # status keeps track of the current action and direction of the player
        self.display_surface = pygame.display.get_surface()

        # attacking monitors whether or not the entity is attacking
        # attack mechanics not currently implemented
        self.attacking = False

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = ENTITY_SPEED
        self.frame_index = 0
        self.animation_speed = 0.15

        # collisions
        self.obstacle_sprites = obstacle_sprites

        # groups
        self.member_groups: List[pygame.sprite.Group] = groups

    def import_assets(self, root_dir: str):
        for folder in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder)
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

    def input(self):
        pass

    def move(self, speed: float) -> None:
        # normalise the direction vector so both diagonal speeds always have a magnitude of 1
        if self.direction.magnitude() != 0: self.direction = self.direction.normalize()

        # update horizontal velocity
        self.move_x(speed)
        # check for horizontal collision
        self.collision("horizontal")

        # update vertical velocity
        self.move_y(speed)
        # check for vertical collision
        self.collision("vertical")

    def move_x(self, speed: float) -> None:
        """ updates x coordinate of the entity """
        self.rect.x += self.direction.x * speed

    def move_y(self, speed: float) -> None:
        """ updates y coordinate of the entity """
        self.rect.y += self.direction.y * speed

    def collision(self, direction: str) -> None:
        obstacles: List[pygame.sprite.Sprite] = [sprite for sprite in self.obstacle_sprites if sprite != self]

        def horizontal_collision():
            for sprite in obstacles:
                # print(f"sprite {sprite}, self {self}")
                if sprite.rect.colliderect(self.rect):
                    # player moving to the right
                    if self.direction.x > 0: self.rect.right = sprite.rect.left

                    # player moving to the left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

        def vertical_collision():
            for sprite in obstacles:
                if sprite.rect.colliderect(self.rect):
                    # player moving to the down
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top

                    # player moving to the up
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

        collision_type_map: Dict[str, Callable] = {"horizontal": horizontal_collision, "vertical": vertical_collision}

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
