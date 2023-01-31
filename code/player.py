import os
import pygame
from settings import *
from utils import get_spawn_point_id
from entity import Entity
from observable import Observable
from observer import Observer


class Player(Entity, Observable):
    def __init__(self, pos: tuple[float, float], image_path: str, groups: list[pygame.sprite.Sprite],
                 obstacle_sprites: pygame.sprite.Group, transition_sprites: pygame.sprite.Group,
                 spawn_points: pygame.sprite.Group, initial_level_code: int, **kwargs):

        super().__init__(pos, image_path, groups, obstacle_sprites)

        # general setup
        self.current_level_code = initial_level_code

        # collisions
        self.transition_sprites = transition_sprites
        self.spawn_points = spawn_points

        # temp
        self.next_level_spawn_id = None

        # add observers
        self.__set_observers(kwargs.get("observers", None))

    def __set_observers(self, observers: list[Observer] = None):
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
        self.add(new_visible_sprites_group)
        self.obstacle_sprites = new_obstacle_sprites_group
        self.transition_sprites = new_transition_sprites_group
        self.spawn_points = new_spawn_point_group

    def input(self):
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

    def get_current_level_code(self) -> int:
        return self.current_level_code

    # Override
    def move(self, speed: float):
        # check for collision with a TransitionBox object
        self.collision("transition")

        # call move method from entity class
        super(Player, self).move(speed)

    # Override
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

    # Override
    def update(self):
        self.input()
        self.get_status()
        self.animate()
        self.move(self.speed)
