import pygame
from settings import *
from entity import Entity
from typing import Optional, Union, List, TYPE_CHECKING, Tuple
from a_star import a_star

if TYPE_CHECKING:
    from tile import Tile
    from level import Level, YSortCameraGroup
    from player import Player


class Enemy(Entity):
    def __init__(self, pos: tuple[float, float], asset_image_root_dir_path: str, level: "Level",
                 groups: List[Union["YSortCameraGroup", pygame.sprite.Sprite]],
                 obstacle_sprites: pygame.sprite.Group) -> None:

        super().__init__(pos, asset_image_root_dir_path, groups, obstacle_sprites)

        # store the level object in associated with the instance
        self.level: Level = level
        # start enemy moving upwards
        self.direction = pygame.math.Vector2(0, -1)
        self.status = "up"

        # change default speed
        self.speed: float = ENEMY_SPEED

        """
        define enemy aggression circle radius.
        Variable name self.radius is required for pygame.sprite.collide_circle method to work.
        https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_circle
        """
        self.radius: int = ENEMY_ATTACK_RADIUS

    # Overrides parent method
    def patrol(self, speed: Union[float, int]) -> None:
        current_tile: Tile = self.level.get_tile(self.rect.center)

        def update_status() -> None:
            if self.direction.y == -1:
                self.status = "up"
            elif self.direction.y == 1:
                self.status = "down"

            if self.direction.x == -1:
                self.status = "left"
            elif self.direction.x == 1:
                self.status = "right"

        if current_tile:
            # moving upwards
            if self.direction.y == -1:
                next_tile_coords: Tuple[float, float] = \
                    (current_tile.rect.centerx, current_tile.rect.centery - TILE_SIZE)

            # moving downwards
            else:
                next_tile_coords: Tuple[float, float] =\
                    (current_tile.rect.centerx, current_tile.rect.centery + TILE_SIZE)

            # if the next tile isn't pathable reverse the y direction
            if not self.level.get_tile(next_tile_coords).is_pathable():
                self.direction.y *= -1
                update_status()

            # call parent method to handle actual movement logic
            super(Enemy, self).move(speed)

    # type hint Player causing an error for the player parameter using Forward referencing to solve problem
    def is_in_circle_of_aggression(self, player: "Player") -> bool:
        """
        checks to see if any point of the player rect lies within a circle of radius self.radius
        centred at the enemy rect's centre
        """
        return pygame.sprite.collide_circle(self, player)

    # Overrides parent method
    def update(self) -> None:
        self.is_in_circle_of_aggression(self.level.player)
        super().update()
