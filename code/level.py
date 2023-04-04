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

        self.level_groups: List[pygame.sprite.Group] = [self.visible_sprites, self.obstacle_sprites, self.transition_sprites,
                                                  self.spawn_points]

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
                SpawnPoint(pos=position, level=self, groups=[self.spawn_points], spawn_point_id=spawn_point.id,
                           spawn_point_type=spawn_point.spawn_point_type)

        def create_enemies() -> None:
            for spawn_point in self.spawn_points:
                if spawn_point.get_spawn_point_type() == "enemy":
                    enemy_spawn_point: SpawnPoint = spawn_point
                    Enemy(spawn_point=enemy_spawn_point, asset_image_root_dir_path=ENEMY_IMAGES_FILE_PATH, level=self,
                          groups=[self.visible_sprites, self.obstacle_sprites], obstacle_sprites=self.obstacle_sprites)

        create_tile_objects()
        create_collidable_objects()
        create_transition_objects()
        create_spawn_point_objects()
        create_enemies()

    def get_level_groups(self) -> list[pygame.sprite.Group]:
        return self.level_groups

    def set_player(self, player: Player) -> None:
        self.player = player

    def get_tile(self, pos: Tuple[Union[float, int], Union[float, int]]) -> Optional[Tile]:
        """ Calculates the row and column number of the position argument and returns the tile at that position
            if there is no tile at the calculated position returns None """
        row: int = pos[0] // TILE_SIZE
        col: int = pos[1] // TILE_SIZE

        return self.tile_map.get((row, col), None)

    def get_neighbours(self, tile: Tile, directions: List[Tuple[int, int]]):
        """
              Returns immediately neighbouring tiles of the tile parameter object, in the directions
              provided as argument if the neighbour tile exist on the map.
          """

        neighbours: List[Tile] = []

        row: int = tile.rect.centerx // TILE_SIZE
        col: int = tile.rect.centery // TILE_SIZE

        for direction in directions:
            neighbour = self.tile_map.get((row + direction[0], col + direction[1]), None)
            if neighbour:
                neighbours.append(neighbour)

        return neighbours

    def get_cartesian_neighbours(self, tile: Tile) -> Optional[List[Tile]]:
        """
            Returns immediately neighbouring tiles in the cartesian directions of the tile parameter object
            if the neighbour tile exist on the map.
        """

        # Cartesian directions only NO DIAGONALS
        directions: List[Tuple[int, int]] = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        return self.get_neighbours(tile, directions)

    def get_all_neighbours(self, tile: Tile) -> Optional[List[Tile]]:
        """
            Returns all immediately neighbouring tiles of the tile parameter object (four cardinal directions
            plus diagonals) if the neighbour tile exist on the map.
        """

        # up, up-right, right, down-right, down, down-left, left, up-left
        directions: List[Tuple[int, int]] = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        return self.get_neighbours(tile, directions)

    def get_pathable_neighbours(self, tile: Tile) -> Optional[List[Tile]]:
        """
            Returns all PATHABLE immediately neighbouring tiles (cartesian neighbours only)
             if the tile parameter object if the neighbour tile exist on the map.
        """

        neighbours: Union[List[Tile], None] = self.get_cartesian_neighbours(tile)
        return [neighbour for neighbour in neighbours if neighbour is not None and neighbour.is_pathable()]

    def get_alive_enemies(self) -> Optional[List[Enemy]]:
        """
        Returns a list of alive Enemy objects present on the Level.
        An Enemy object is alive if it is a member of the obstacle_sprites group
        """

        enemies: List[Enemy] = []
        for sprite in self.obstacle_sprites:
            if type(sprite) == Enemy:
                enemies.append(sprite)

        return enemies

    def make_eligible_enemies_attack_player(self):
        for enemy in self.get_alive_enemies():
            enemy.attack_player()

    def enemy_scan(self):
        """
            Checks if the players current position lies within any enemy sprites circle of attack.
            If true the enemy's movement_behaviour_mode is set to "attack" meaning the enemy sprite will not
            move, but it will face towards the player.
            Else if the players current position lies within any enemy sprites circle of aggression but not within
            the circle of attack, the enemy's movement_behaviour_mode is set to "seek" meaning the enemy sprite will
            path towards the player until the player lies within the circle of attack.
        """

        for enemy in self.get_alive_enemies():
            if enemy.is_in_circle_of_attack(self.player):
                # if the player is in the attack radius DO NOT move and face towards the player
                enemy.set_movement_behaviour_mode("attack")
                # set the current time for the attack cooldown function
                enemy.attack_time = pygame.time.get_ticks()

            elif enemy.is_in_circle_of_aggression(self.player):
                # if the player is in the aggression radius but not in the attack radius, path towards player
                enemy.set_movement_behaviour_mode("seek")

    def de_spawn_dead_entities(self) -> None:
        def garbage_collection_countdown_time_elapsed(entity: Entity) -> bool:
            current_time: int = pygame.time.get_ticks()
            if entity.time_of_death:
                return current_time - entity.time_of_death >= DEAD_OBJECT_CLEARANCE_COUNTDOWN_TIME
            return False

        for sprite in self.obstacle_sprites:
            if isinstance(sprite, Entity) and garbage_collection_countdown_time_elapsed(sprite):
                entity: Entity = sprite
                entity.kill()
                del entity  # eventually add object to object pool instead.

    def run(self) -> None:
        try:
            self.visible_sprites.custom_draw(self.player)
        except Exception as e:
            print(e)

        self.visible_sprites.update()

        try:
            enemy_sprite = [x for x in self.visible_sprites if type(x) == Enemy][0]
            # debug(enemy_sprite.status)
            debug(f"player health {self.player.health_points}, enemy_status {enemy_sprite.status}")
        except:
            pass


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
