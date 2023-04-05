import os
import pygame
from settings import *
from collections import defaultdict
from typing import List, Dict, Callable, Tuple, TYPE_CHECKING, Optional
from utils import get_spawn_point_object_data, get_spawn_point_id
from observable import Observable
import pathlib

if TYPE_CHECKING:
    from spawnPoint import SpawnPoint


class Entity(pygame.sprite.Sprite):
    def __init__(self, spawn_point: "SpawnPoint", asset_images_root_dir_path: str, groups: List[pygame.sprite.Group],
                 obstacle_sprites: pygame.sprite.Group) -> None:

        super().__init__(groups)
        # general setup
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        default_image_path: str = os.path.join(asset_images_root_dir_path, "down_idle", "down_idle_1.png")
        self.spawn_point: "SpawnPoint" = spawn_point
        self.image: pygame.Surface = pygame.image.load(default_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  # scale image to match screen size
        self.rect: pygame.Rect = self.image.get_rect(topleft=self.spawn_point.get_associated_tile().rect.topleft)

        # animations
        self.animations: Dict[str, List[pygame.Surface]] = defaultdict(lambda: [])
        self.import_assets(asset_images_root_dir_path)
        self.status: str = "down"  # status keeps track of the current action and direction of the player
        self.animation_modes: Dict[str, Callable] = {
            "alive": self.alive_animation,
            "dead": self.dead_animation
        }

        self.animation_mode: Callable = self.alive_animation

        # stats
        self.health_points: int = DEFAULT_HEALTH_POINTS
        self.time_of_death: Optional[int] = None

        # attack
        self.attacking: bool = False
        self.attack_cooldown_time: int = DEFAULT_ATTACK_COOLDOWN_TIME
        self.attack_time: Optional[int] = None

        # movement
        self.direction: pygame.math.Vector2 = pygame.math.Vector2()
        self.speed: float = ENTITY_SPEED
        self.frame_index: int = 0
        self.animation_speed: float = 0.15

        # collisions
        self.obstacle_sprites: pygame.sprite.Group = obstacle_sprites

        # groups
        self.member_groups: List[pygame.sprite.Group] = groups

    def import_assets(self, root_dir: str) -> None:
        for folder in os.listdir(root_dir):
            folder_path: str = os.path.join(root_dir, folder)
            for image in os.listdir(folder_path):
                image_path: str = os.path.join(folder_path, image)
                surf: pygame.Surface = pygame.image.load(image_path).convert_alpha()
                # scale player image up to fit map size
                surf = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
                self.animations[folder].append(surf)

    def get_status(self) -> None:
        if not self.is_dead():
            # idle status
            if all(velocity == 0 for velocity in self.direction) and \
                    all(word not in self.status for word in ["idle", "attack"]):
                self.status += "_idle"

            if self.attacking:
                # self.direction.x = 0
                # self.direction.y = 0
                if "attack" not in self.status:
                    if "idle" in self.status:
                        self.status = self.status.replace("_idle", "_attack")
                    else:
                        self.status += "_attack"

            # if not attacking remove attack from status (if attack is in status).
            else:
                if "attack" in self.status:
                    self.status = self.status.replace("_attack", "")

    def is_dead(self) -> bool:
        return self.status == "dead"

    def is_alive(self) -> bool:
        return not self.is_dead()

    def reduce_health(self, damage: float) -> None:
        self.health_points -= damage

    def input(self) -> None:
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
        """
            checks for object collision with other collidable objects in the obstacle sprites group
            the objects position will be reset upon collision to boundary between the colliding objects in the movement
            direction, this prevents clipping between the two objects.
        """

        # fiter out the calling object if it is present in the obstacle_sprites group
        # prevents an object checking for collisions with itself, which causes a movement bug
        obstacles: List[pygame.sprite.Sprite] = [sprite for sprite in self.obstacle_sprites if sprite != self]

        def horizontal_collision():
            for sprite in obstacles:
                # print(f"sprite {sprite}, self {self}")
                if sprite.rect.colliderect(self.rect):
                    # player moving to the right
                    if self.direction.x > 0: self.rect.right = sprite.rect.left

                    # player moving to the left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

                    # if the sprite object is of type Observable notify its Observers of the collision
                    if isinstance(sprite, Observable):
                        sprite.observable_notify()

        def vertical_collision():
            for sprite in obstacles:
                if sprite.rect.colliderect(self.rect):
                    # player moving to the down
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top

                    # player moving to the up
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

                    # if the sprite object is of type Observable notify its Observers of the collision
                    if isinstance(sprite, Observable):
                        sprite.observable_notify()

        collision_type_map: Dict[str, Callable] = {"horizontal": horizontal_collision, "vertical": vertical_collision}

        collision_type_map[direction]()

    def animate(self) -> None:
        self.animation_mode()

    def alive_animation(self) -> None:
        animation: List[pygame.Surface] = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): self.frame_index = 0

        # change the current player image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def dead_animation(self) -> None:
        animation: List[pygame.Surface] = self.animations[self.status]
        final_frame_index: int = len(animation) - 1

        # loop over frame index
        if self.frame_index < len(animation):
            self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = final_frame_index

        # change the current player image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def attack(self) -> None:
        pass

    def update(self) -> None:
        if not self.is_dead():
            self.input()
            self.get_status()
        self.animate()
        if not self.is_dead():
            self.move(self.speed)
