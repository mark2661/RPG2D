import pygame
from typing import Dict, Tuple, Union, Optional, List

import pytmx.pytmx
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Tile
from player import Player
from hitbox import HitBox
from transitionBox import TransitionBox
from spawnPoint import SpawnPoint
from debug import debug
from enemy import Enemy
from entity import Entity


class Level:
    def __init__(self, map_path: str, player: Player = None) -> None:
        # load map
        self.tmx_data: pytmx.pytmx.TiledMap = load_pygame(map_path)

        # get display surface
        self.display_surface: pygame.Surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites: YSortCameraGroup = YSortCameraGroup()
        self.obstacle_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.transition_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.spawn_points: pygame.sprite.Group = pygame.sprite.Group()

        # tile map provides a quick way to access tile objects based on their row, col position (not coords) on the grid
        # e.g the tile in the top left would have row = 0 and col = 0
        self.tile_map: Dict[Tuple[int, int], Tile] = dict()

        # initialise map
        self.create_map()

        # set player
        self.player: Player = player


    def create_map(self) -> None:
        """ This function creates individual tile objects for each tile in the .tmx file assigned to self.tmx_data
            and adds them to a pygame sprite group
        """

        # catch ValueError if Pathing layer doesn't exist
        try:
            pathable_tiles: List[pytmx.pytmx.TiledObject] = list(self.tmx_data.get_layer_by_name("Pathing").tiles())
        except ValueError:
            pathable_tiles = []

        def create_tile_objects() -> None:
            def is_pathable_tile(tile_top_left_pos: tuple[float, float]) -> bool:
                """
                    if the tile has the same world coordinates as a tile in pathable tiles then that tile is pathable
                    since the tiles are the same.
                """
                for index, pathable_tile in enumerate(pathable_tiles):
                    pathable_tile_x: float
                    pathable_tile_y: float
                    pathable_tile_x, pathable_tile_y, _ = pathable_tile
                    if pathable_tile_x == tile_top_left_pos[0] and pathable_tile_y == tile_top_left_pos[1]:
                        pathable_tiles.pop(index)  # if found remove the tile to speed up subsequent checks
                        return True

                return False

            for layer in self.tmx_data.visible_layers:
                if hasattr(layer, "data"):
                    for x, y, surf in layer.tiles():
                        position: Tuple[float, float] = (x * TILE_SIZE, y * TILE_SIZE)
                        new_tile: Tile = Tile(position, surf, [self.visible_sprites],
                                              layer.name, is_pathable_tile((x, y)))
                        self.tile_map[(x, y)] = new_tile

        def create_collidable_objects() -> None:
            collidable_objects: pytmx.pytmx.TiledObjectGroup = self.tmx_data.get_layer_by_name("Collision_Objects")
            for collidable_object in collidable_objects:
                position: Tuple[float, float] = (collidable_object.x, collidable_object.y)
                size: Tuple[float, float] = (collidable_object.width, collidable_object.height)
                HitBox(position, size, [self.obstacle_sprites])

        def create_transition_objects() -> None:
            transition_objects: pytmx.pytmx.TiledObjectGroup = self.tmx_data.get_layer_by_name("Transition_Objects")
            for transition_object in transition_objects:
                position: Tuple[float, float] = (transition_object.x, transition_object.y)
                size: Tuple[float, float] = (transition_object.width, transition_object.height)
                TransitionBox(position, size, [self.transition_sprites], transition_object.transition_code)

        def create_spawn_point_objects() -> None:
            spawn_point_objects: pytmx.pytmx.TiledObjectGroup = self.tmx_data.get_layer_by_name("Spawn_Points")
            for spawn_point in spawn_point_objects:
                position: Tuple[float, float] = (spawn_point.x, spawn_point.y)
                SpawnPoint(position, [self.spawn_points], spawn_point.id)

        # only creates a single enemy per level for testing at the moment
        def create_enemies():
            enemy_spawn_position: Tuple[float, float] = (
                (self.display_surface.get_width() // 2) + 500, (self.display_surface.get_height() // 2) + 25)
            Enemy(pos=enemy_spawn_position, asset_image_root_dir_path=ENEMY_IMAGES_FILE_PATH, level=self,
                  groups=[self.visible_sprites, self.obstacle_sprites], obstacle_sprites=self.obstacle_sprites)

        create_tile_objects()
        create_collidable_objects()
        create_transition_objects()
        create_spawn_point_objects()
        create_enemies()

    def get_level_groups(self) -> list[pygame.sprite.Group]:
        return [self.visible_sprites, self.obstacle_sprites, self.transition_sprites, self.spawn_points]

    def set_player(self, player: Player) -> None:
        self.player = player

    def get_tile(self, pos: Tuple[Union[float, int], Union[float, int]]) -> Optional[Tile]:
        """ Calculates the row and column number of the position argument and returns the tile at that position
            if there is no tile at the calculated position returns None """
        row: int = pos[0] // TILE_SIZE
        col: int = pos[1] // TILE_SIZE

        return self.tile_map.get((row, col), None)

    def get_neighbours(self, tile: Tile) -> List[Tile]:
        # up, up_right, right, down_right, down, down_left, left, up_left
        directions: List[Tuple[int, int]] = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        neighbours: List[Tile] = []

        row: int = tile.rect.centerx // TILE_SIZE
        col: int = tile.rect.centery // TILE_SIZE

        for direction in directions:
            neighbour = self.tile_map.get((row + direction[0], col + direction[1]), None)
            if neighbour:
                neighbours.append(neighbour)

        return neighbours






    def run(self) -> None:
        try:
            self.visible_sprites.custom_draw(self.player)
        except Exception as e:
            print(e)

        self.visible_sprites.update()
        debug(self.player.rect.center)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        # general setup
        super().__init__()
        self.display_surface: pygame.Surface = pygame.display.get_surface()
        self.half_width: int
        self.half_height: int
        self.half_width, self.half_height = self.display_surface.get_width() // 2, self.display_surface.get_height() // 2
        self.offset: pygame.math.Vector2 = pygame.math.Vector2()

    def custom_draw(self, player: Player) -> None:
        def draw_floor_tiles(tiles: list[pygame.sprite.Sprite]) -> None:
            # draw floor tiles before non-floor tiles (painters algorithm)
            for tile in tiles:
                offset: float = tile.rect.topleft - self.offset
                self.display_surface.blit(tile.image, offset)

        def draw_non_floor_tiles(tiles: list[pygame.sprite.Sprite]) -> None:
            # draw non-floor tiles on top of floor tiles using Y-sort algorithm
            for tile in sorted(tiles, key=lambda tile: tile.rect.centery):
                offset: float = tile.rect.topleft - self.offset
                self.display_surface.blit(tile.image, offset)

        # offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # separate floor tiles and non-floor tiles
        floor_tiles: List[Tile] = [sprite for sprite in self.sprites() if not isinstance(sprite, Entity) and
                                   sprite.tiled_layer in ["Ground", "Carpet", "Shadows"]]

        non_floor_tiles: List[pygame.sprite.Sprite] = [sprite for sprite in self.sprites() if isinstance(sprite, Entity)
                                                       or
                                                       sprite.tiled_layer not in ["Ground", "Carpet", "Shadows"]]

        draw_floor_tiles(floor_tiles)
        draw_non_floor_tiles(non_floor_tiles)

    def regular_draw(self) -> None:
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
