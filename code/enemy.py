from settings import *
from entity import Entity
from typing import Optional, Union, List, TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from tile import Tile
    from level import Level, YSortCameraGroup
    from player import Player


class Enemy(Entity):
    def __init__(self, pos: tuple[float, float], asset_image_root_dir_path: str, level: "Level",
                 groups: List[Union["YSortCameraGroup", pygame.sprite.Sprite]], obstacle_sprites: pygame.sprite.Group):

        super().__init__(pos, asset_image_root_dir_path, groups, obstacle_sprites)

        # store the level object in associated with the instance
        self.level = level
        # start enemy moving upwards
        self.direction = pygame.math.Vector2(0, -1)

        # change default speed
        self.speed = ENEMY_SPEED

        """
        define enemy aggression circle radius.
        Variable name self.radius is required for pygame.sprite.collide_circle method to work.
        https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_circle
        """
        self.radius = ENEMY_ATTACK_RADIUS

    # Overrides parent method
    def move(self, speed: Union[float, int]) -> None:
        current_tile: Tile = self.level.get_tile(self.rect.center)

        if current_tile:
            # moving upwards
            # BUG? for some reason check for == -1 doesn't work (even though that's the upwards direction)
            if self.direction.y == -1:
                next_tile_coords = (current_tile.rect.centerx, current_tile.rect.centery - TILE_SIZE)

            # moving downwards
            else:
                next_tile_coords = (current_tile.rect.centerx, current_tile.rect.centery + TILE_SIZE)

            # if the next tile isn't pathable reverse the y direction
            if not self.level.get_tile(next_tile_coords).is_pathable():
                self.direction.y *= -1

            # call parent method to handle actual movement logic
            super(Enemy, self).move(speed)

    # type hit Player causing an error for the plyer parameter
    def is_in_circle_of_attack(self, player) -> bool:
        """
        checks to see if any point of the player rect lies within a circle of radius self.radius
        centred at the enemy rect's centre
        """
        return pygame.sprite.collide_circle(self, player)

    # Overrides parent method
    def update(self) -> None:
        self.is_in_circle_of_attack(self.level.player)
        super().update()
