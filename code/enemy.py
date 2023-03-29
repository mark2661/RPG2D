import pygame
from settings import *
from entity import Entity
from typing import Optional, Union, List, TYPE_CHECKING, Tuple, Dict, Callable
from a_star import a_star

if TYPE_CHECKING:
    from tile import Tile
    from level import Level, YSortCameraGroup
    from player import Player
    from spawnPoint import SpawnPoint


class Enemy(Entity):
    def __init__(self, spawn_point: "SpawnPoint", asset_image_root_dir_path: str, level: "Level",
                 groups: List[Union["YSortCameraGroup", pygame.sprite.Sprite]],
                 obstacle_sprites: pygame.sprite.Group) -> None:

        super().__init__(spawn_point, asset_image_root_dir_path, groups, obstacle_sprites)

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
            "seek": self.seek,
            "return_to_spawn": self.return_to_spawn_point
        }
        # Default movement behaviour is patrol mode
        self.movement_behaviour_mode: Callable = self.movement_behaviour_modes["patrol"]

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
        Sets the entities direction to a vector pointing
        to the next tile in the path list of pathable Tile objects leading to the players current position.
        """
        path_to_player: Optional[List["Tile"]] = self.get_path_to_player()

        if path_to_player and len(path_to_player) > 1:
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
        else:
            # no path to player exist, return to spawn point
            self.set_movement_behaviour_mode("return_to_spawn")

    def return_to_spawn_point(self, speed: float) -> None:
        """
        Sets the entities direction to a vector pointing
        to the next tile in the path list of pathable Tile objects leading to the entities spawn point.
        """
        path_to_spawn_point: Optional[List["Tile"]] = self.get_path_to_spawn_point()

        if path_to_spawn_point and len(path_to_spawn_point) > 1:
            next_tile: "Tile" = path_to_spawn_point[1]
            x: float = next_tile.rect.centerx - self.rect.centerx
            y: float = next_tile.rect.centery - self.rect.centery
            vector_to_next_tile: pygame.math.Vector2 = pygame.math.Vector2((x, y)).normalize()

            # change direction
            self.direction = vector_to_next_tile
            self.update_status()

            # call parent move method to handle movement logic
            super().move(speed)

        else:
            # entity is either on the destination tile or adjacent to it
            next_tile: "Tile" = path_to_spawn_point[0]
            x: float = next_tile.rect.centerx - self.rect.centerx
            y: float = next_tile.rect.centery - self.rect.centery
            vector_to_next_tile: pygame.math.Vector2 = pygame.math.Vector2((x, y)).normalize()

            # change direction
            self.direction = vector_to_next_tile
            self.update_status()

            # get pathing in the same direction until the destination tile is reached
            while self.level.get_tile(self.rect.midleft) != self.spawn_point.get_associated_tile():
                # call parent move method to handle movement logic
                super().move(speed)

            # reset to original patrol direction (need to change this logic eventually)
            self.direction = pygame.math.Vector2(0, 1)
            self.status = "down"
            self.set_movement_behaviour_mode("patrol")

    def get_path_to_spawn_point(self) -> Optional[List["Tile"]]:
        """
        Calculates a path from the entity to its spawn point (using A*). Returns a list of adjacent pathable tiles,
        if a path exist else None.
        """
        return a_star(start=self.level.get_tile(self.rect.center), end=self.spawn_point.get_associated_tile(),
                      level=self.level)

    def get_path_to_player(self) -> Optional[List["Tile"]]:
        """
        Calculates a path from the entity to the player (using A*). Returns a list of adjacent pathable tiles,
        if a path exist else None.
        """
        return a_star(start=self.level.get_tile(self.rect.center), end=self.level.get_tile(self.level.player.rect.center),
                      level=self.level)

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

    # Overrides parent method
    def update(self) -> None:
        # self.is_in_circle_of_aggression(self.level.player)
        super().update()
