import pygame
from settings import *
from entity import Entity
from typing import Optional, Union, List, TYPE_CHECKING, Tuple, Dict, Callable
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

        # MOVEMENT PARAMETERS
        # start enemy moving upwards
        self.direction = pygame.math.Vector2(0, 1)
        self.status = "down"

        # change default speed
        self.speed: float = ENEMY_SPEED

        # define movement behaviour modes
        self.movement_behaviour_modes: Dict[str: Callable] = {
            "patrol": self.patrol,
            "seek": self.seek
        }
        # Default movement behaviour is patrol mode
        self.movement_behaviour_mode = self.movement_behaviour_modes["patrol"]

        """
        define enemy aggression circle radius.
        Variable name self.radius is required for pygame.sprite.collide_circle method to work.
        https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.collide_circle
        """
        self.radius: int = ENEMY_ATTACK_RADIUS

    def patrol(self, speed: Union[float, int]) -> None:
        """
        checks if the next tile in the current direction (either vertical or horizontal) is a pathable tile
        (a pathable tile is a tile that the entity is allowed to be on).
        if the next tile is pathable the current direction is left unchanged, else reverse the current direction.
        """
        current_tile: Tile = self.level.get_tile(self.rect.center)

        if current_tile:
            if self.is_moving_upwards():
                next_tile_coords: Tuple[float, float] = \
                    (current_tile.rect.centerx, current_tile.rect.centery - TILE_SIZE)

            elif self.is_moving_downwards():
                next_tile_coords: Tuple[float, float] = \
                    (current_tile.rect.centerx, current_tile.rect.centery + TILE_SIZE)

            elif self.is_moving_left():
                next_tile_coords: Tuple[float, float] = \
                    (current_tile.rect.centerx - TILE_SIZE, current_tile.rect.centery)

            # moving right
            else:
                next_tile_coords: Tuple[float, float] = \
                    (current_tile.rect.centerx + TILE_SIZE, current_tile.rect.centery)

            # if the next tile isn't pathable reverse the direction
            if not self.level.get_tile(next_tile_coords).is_pathable():
                """
                since either x or y is = 0 (cartesian movement only on patrol mode) it's ok to reverse both the
                x and y components of the vector regardless of whether the entity is moving horizontally or vertically
                """
                self.direction *= -1
                self.update_status()

            # call parent method to handle actual movement logic
            super().move(speed)

    def is_moving_upwards(self) -> bool:
        return self.direction.y == -1 and self.direction.x == 0

    def is_moving_downwards(self) -> bool:
        return self.direction.y == 1 and self.direction.x == 0

    def is_moving_left(self) -> bool:
        return self.direction.x == -1 and self.direction.y == 0

    def is_moving_right(self) -> bool:
        return self.direction.x == 1 and self.direction.y == 0

    def is_moving_diagonally_with_larger_vertical_component(self) -> bool:
        return abs(self.direction.y) >= abs(self.direction.x)

    def is_moving_diagonally_with_larger_horizontal_component(self) -> bool:
        return abs(self.direction.x) > abs(self.direction.y)

    def update_status(self) -> None:
        """
        updates the entities status variable which is used to select the correct image to be displayed for the
        current position
        """

        if self.is_moving_upwards():
            self.status = "up"
        elif self.is_moving_downwards():
            self.status = "down"
        elif self.is_moving_left():
            self.status = "left"
        elif self.is_moving_right():
            self.status = "right"

        # diagonal movement
        elif self.is_moving_diagonally_with_larger_vertical_component():
            self.status = "down" if self.direction.y > 0 else "up"
        elif self.is_moving_diagonally_with_larger_horizontal_component():
            self.status = "right" if self.direction.x > 0 else "left"

    # not fully implemented still in testing phase and still buggy
    def seek(self, speed: float) -> None:
        """
        calculates a path from the entity to the player and sets the entities direction to a vector pointing
        to the next tile in the path list.
        """
        path_to_player: List[Tile] = a_star(grid=[tile for tile in self.level.tile_map.values() if tile.is_pathable()],
                                            start=self.level.get_tile(self.rect.center),
                                            end=self.level.get_tile(self.level.player.rect.center),
                                            level=self.level)
        # print(path_to_player)
        if path_to_player and len(path_to_player) >= 1:
            # vector between two points = vectorB - vectorA
            next_tile: Tile = path_to_player[1]
            x: float = next_tile.rect.centerx - self.rect.centerx
            y: float = next_tile.rect.centery - self.rect.centery
            vector_to_next_tile: pygame.math.Vector2 = pygame.math.Vector2((x, y)).normalize()

            # change direction
            self.direction = vector_to_next_tile
            self.update_status()

            # call parent move method to handle movement logic
            super().move(speed)

    # Overrides parent method
    def move(self, speed: float) -> None:
        self.movement_behaviour_mode(speed)

    def set_movement_behaviour_mode(self, mode_code: str) -> None:
        self.movement_behaviour_mode = self.movement_behaviour_modes[mode_code]

    # type hint Player causing an error for the player parameter using Forward referencing to solve problem
    def is_in_circle_of_aggression(self, player: "Player") -> bool:
        """
        checks to see if any point of the player rect lies within a circle of radius self.radius
        centred at the enemy rect's centre
        """
        return pygame.sprite.collide_circle(self, player)

    # Overrides parent method
    def update(self) -> None:
        # self.is_in_circle_of_aggression(self.level.player)
        super().update()
