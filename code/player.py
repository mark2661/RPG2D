import os
import pygame
from settings import *
from utils import get_spawn_point_id
from livingentity import LivingEntity
from observable import Observable
from observer import Observer
from typing import Tuple, TYPE_CHECKING, List, Dict
from enemy import Enemy

if TYPE_CHECKING:
    from spawnPoint import SpawnPoint
    from tile import Tile


class Player(LivingEntity, Observable):
    """
       The Player class represents the player character in the game. It extends the LivingEntity class and implements
       the Observable interface. The class handles player input, movement, collisions, attacks, and health management.
    """
    def __init__(self, spawn_point: "SpawnPoint", asset_images_root_dir_path: str, groups: list[pygame.sprite.Sprite],
                 obstacle_sprites: pygame.sprite.Group, transition_sprites: pygame.sprite.Group,
                 spawn_points: pygame.sprite.Group, initial_level_code: int, **kwargs):

        # call parent class constructors
        LivingEntity.__init__(self, spawn_point, asset_images_root_dir_path, groups, obstacle_sprites)
        Observable.__init__(self)

        # general setup
        self.current_level_code = initial_level_code

        # stats
        self.health_points = PLAYER_HEALTH_POINTS  # overrides parent variable

        # collisions
        self.transition_sprites = transition_sprites
        self.spawn_points = spawn_points

        # attack
        self.attack_cooldown_time = PLAYER_ATTACK_COOLDOWN_TIME

        # temp
        self.next_level_spawn_id = None

        # add observers
        self.__set_observers(kwargs.get("observers", None))

    def __set_observers(self, observers: list[Observer] = None):
        """
           Subscribes the provided observers to the player, allowing them to receive notifications when the
           player's position changes.
        """
        if observers:
            for observer in observers:
                self.observable_add(observer)

    def set_groups(self, groups: list[pygame.sprite.Group]):
        new_visible_sprites_group = groups[0]
        new_obstacle_sprites_group = groups[1]
        new_transition_sprites_group = groups[2]
        new_spawn_point_group = groups[3]

        # remove player from previous visible sprites group
        self.kill()

        # update groups
        self.add(new_visible_sprites_group, new_obstacle_sprites_group)
        self.obstacle_sprites = new_obstacle_sprites_group
        self.transition_sprites = new_transition_sprites_group
        self.spawn_points = new_spawn_point_group

    # Override
    def input(self):
        """
           Handles player keyboard inputs for movement and attacking. It sets the player's direction and status
           based on the pressed keys. When the attack key is pressed, it triggers the attack method.
        """
        keys = pygame.key.get_pressed()
        up, down, left, right = keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]

        if up:
            self.direction.y = -1
            self.status = "up"

        elif down:
            self.direction.y = 1
            self.status = "down"

        else:
            self.direction.y = 0

        if right:
            self.direction.x = 1
            self.status = "right"

        elif left:
            self.direction.x = -1
            self.status = "left"

        else:
            self.direction.x = 0

        # attack inputs
        # melee
        if keys[pygame.K_l] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.attack()

    def get_current_level_code(self) -> int:
        return self.current_level_code

    # Override
    def move(self, speed: float) -> None:
        """ updates players x and y coordinates. Also checks for collisions with objects
            and triggers associated events
        """
        old_position: Tuple[float, float] = self.rect.center

        # check for collision with a TransitionBox object
        self.collision("transition")

        # call super method to handle movement logic
        super().move(speed)

        # if position has changed notify observers
        if self.rect.center != old_position:
            self.observable_notify()

    # Override parent method
    def collision(self, direction: str):
        def transition_collision():
            for transition_sprite in self.transition_sprites:
                if transition_sprite.rect.colliderect(self.rect):
                    self.current_level_code = transition_sprite.get_new_level_code()
                    self.next_level_spawn_id = get_spawn_point_id(transition_sprite.get_transition_code())

        collision_type_map = {
            "transition": transition_collision,
            "horizontal": lambda: super(Player, self).collision("horizontal"),
            "vertical": lambda: super(Player, self).collision("vertical")
        }

        collision_type_map[direction]()

    # Override parent method
    def attack(self) -> None:
        """
        Removes health points from any attackable objects where the Player is within their circle of attack, if
        the Player and the attackable object are facing one another.
        """
        valid_direction_combinations: Dict[str, str] = {"up": "down",
                                                        "right": "left",
                                                        "down": "up",
                                                        "left": "right"
                                                        }

        for sprite in self.obstacle_sprites:
            if type(sprite) == Enemy:
                enemy: Enemy = sprite
                if enemy.is_in_circle_of_attack(self):
                    for direction in valid_direction_combinations:
                        if enemy.status.startswith(direction) and self.status.startswith(
                                valid_direction_combinations[direction]):
                            enemy.reduce_health(damage=PLAYER_ATTACK_DAMAGE)

    def attack_cooldown(self) -> None:
        current_time: int = pygame.time.get_ticks()

        def cooldown_elapsed() -> bool:
            return current_time - self.attack_time >= self.attack_cooldown_time

        if self.attacking and cooldown_elapsed():
            self.attacking = False

    def check_if_player_should_be_dead(self) -> None:
        """
           Checks if the player's health points have dropped to or below zero and marks the player as dead if
           necessary, by setting the player's status instance attribute to "dead".
        """

        def kill_player() -> None:
            """
            Sets the Entities status to dead,  Also changes the animation_mode to "dead" which plays the dying
            animations for the Entity
            """
            self.status = "dead"
            # set animation mode (in parent class) to "dead"
            self.animation_mode = self.animation_modes["dead"]
            self.frame_index = 0  # reset the frame index so the death animation starts from the first frame.

        if "dead" not in self.status and self.health_points <= 0:
            kill_player()

    # Override parent method
    def update(self):
        self.attack_cooldown()
        self.check_if_player_should_be_dead()
        super().update()
