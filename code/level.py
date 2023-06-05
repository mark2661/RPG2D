import pygame
from typing import Dict, Tuple, Union, Optional, List, TYPE_CHECKING

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
from livingentity import LivingEntity
from abstractEntity import AbstractEntity
from enemyObjectPool import EnemyObjectPool
from healthObject import HealthObject
from objectEntity import ObjectEntity
from objectPoolHandler import ObjectPoolHandler

if TYPE_CHECKING:
    from levelHandler import LevelHandler
    from objectPool import ObjectPool


class Level:
    """
       The Level class encapsulates the logic and functionality related to a game level. It is responsible for creating
       and managing various objects within the level, including tiles, obstacles, spawn points, enemies, and transition
       objects. The class loads map data from a file and uses it to create in-game objects based on the data provided.
    """
    def __init__(self, map_path: str, level_handler: "LevelHandler", player: Player = None) -> None:
        self.level_handler: "LevelHandler" = level_handler
        # load map
        self.tmx_data: pytmx.pytmx.TiledMap = load_pygame(map_path)

        # get display surface
        self.display_surface: pygame.Surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites: YSortCameraGroup = YSortCameraGroup()
        self.obstacle_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.transition_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.spawn_points: pygame.sprite.Group = pygame.sprite.Group()

        self.level_groups: List[pygame.sprite.Group] = [self.visible_sprites, self.obstacle_sprites,
                                                        self.transition_sprites,
                                                        self.spawn_points]

        # tile map provides a quick way to access tile objects based on their row, col position (not coords) on the grid
        # e.g the tile in the top left would have row = 0 and col = 0
        self.tile_map: Dict[Tuple[int, int], Tile] = dict()
        self.object_pool_handler: ObjectPoolHandler = ObjectPoolHandler()

        # initialise map
        self.create_map()

        # set player
        self.player: Player = player

    def create_map(self) -> None:
        """
        This function crates in-game objects representing tiles and objects defined in the layers withing the levels
        map-file.
        """

        # catch ValueError if Pathing layer doesn't exist
        try:
            pathable_tiles: List[pytmx.pytmx.TiledObject] = list(self.tmx_data.get_layer_by_name("Pathing").tiles())
        except ValueError:
            pathable_tiles = []

        def create_tile_objects() -> None:
            """
            Iterates over visible layers from the games tile map data and creates Tile objects.
            For each tile, the code calculates its position based on its coordinates in the map-file and creates a new
            Tile object using position and image data from the map file Tile objects are then stored in a
            tile_map dictionary using the tile's coordinates as the keys for quick access.
            """
            def is_pathable_tile(tile_top_left_pos: tuple[float, float]) -> bool:
                """
                    Checks to see whether the tile was declared as pathable in the map-file. A tile is pathable if their
                    exist a tile in the non-visible pathable tiles layer of the map-file with the same world
                    coordinates.
                    Pathable tiles are tiles which non-player entities are permitted to move on.
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
            """
            Creates collidable objects or obstacles based on objects defined in the "Collision_Objects"
            layer of the games map data. It iterates over the objects in the objects defined in the layer and retrieves
            their positions and sizes, and creates corresponding HitBox objects to represent the collidable objects in
            the game.
            """
            collidable_objects: pytmx.pytmx.TiledObjectGroup = self.tmx_data.get_layer_by_name("Collision_Objects")
            for collidable_object in collidable_objects:
                position: Tuple[float, float] = (collidable_object.x, collidable_object.y)
                size: Tuple[float, float] = (collidable_object.width, collidable_object.height)
                HitBox(position, size, [self.obstacle_sprites])

        def create_non_collidable_objects() -> None:
            """
             Creates non_collidable objects based on objects defined in the non-collidable layers of the
             games map data. It iterates over non-collidable layers in the map-file and calls corresponding helper
             functions to create in-game objects representing the objects in the map-file layer, based on the data from
             the map-file object.
            """
            def create_health_objects() -> None:
                """
                   Creates HealthObject's based on objects defined in the map-file layer named
                   "Health_Objects". It iterates over the objects in the layer, retrieves their coordinates,
                   and request and initialises in-game HealthObject instances from an object pool using the
                   object_pool_handler.
                """
                health_objects: pytmx.pytmx.TiledObjectGroup = self.tmx_data.get_layer_by_name("Health_Objects")
                for health_object in health_objects:
                    object_coordinates: Tuple[float, float] = (health_object.x, health_object.y)
                    self.object_pool_handler.acquire(HealthObject, position=object_coordinates, level=self)

            create_health_objects()

        def create_transition_objects() -> None:
            """
            Creates transition objects (objects that can trigger events when collided with. i.e a level change or
            cut scene) from objects defined in an object layer named "Transition_Objects" in the map-file.
            The function iterates over the objects in the map-file layer, retrieves their positions, sizes, and
            transition codes (a numeric value mapping the object to an event), and creates corresponding in-game
            TransitionBox objects.
            """
            transition_objects: pytmx.pytmx.TiledObjectGroup = self.tmx_data.get_layer_by_name("Transition_Objects")
            for transition_object in transition_objects:
                position: Tuple[float, float] = (transition_object.x, transition_object.y)
                size: Tuple[float, float] = (transition_object.width, transition_object.height)
                TransitionBox(position, size, [self.transition_sprites], transition_object.transition_code)

        def create_spawn_point_objects() -> None:
            """
               Creates SpawnPoint objects based on objects defined in the map-file object layer named "Spawn_Points".
               For each object in the layer the function, retrieves their position, and creates corresponding in-game
               SpawnPoint objects.
            """
            spawn_point_objects: pytmx.pytmx.TiledObjectGroup = self.tmx_data.get_layer_by_name("Spawn_Points")
            for spawn_point in spawn_point_objects:
                position: Tuple[float, float] = (spawn_point.x, spawn_point.y)
                SpawnPoint(pos=position, level=self, groups=[self.spawn_points], spawn_point_id=spawn_point.id,
                           spawn_point_type=spawn_point.spawn_point_type)

        def create_enemies() -> None:
            """
            Creates Enemy objects using the levels SpawnPoint objects. The function iterates over the spawn points,
            checks if the spawn point type is "enemy", and acquires instances of the Enemy class from the object
            pool (via the object pool handler).
            """
            for spawn_point in self.spawn_points:
                if spawn_point.get_spawn_point_type() == "enemy":
                    enemy_spawn_point: SpawnPoint = spawn_point
                    op: "ObjectPool" = self.object_pool_handler.object_pools[Enemy.__name__]
                    self.object_pool_handler.acquire(Enemy, spawnPoint=enemy_spawn_point, level=self)

        create_tile_objects()
        create_collidable_objects()
        create_non_collidable_objects()
        create_transition_objects()
        create_spawn_point_objects()
        create_enemies()

    def get_level_groups(self) -> list[pygame.sprite.Group]:
        return self.level_groups

    def set_player(self, player: Player) -> None:
        self.player = player

    def get_tile(self, pos: Tuple[Union[float, int], Union[float, int]]) -> Optional[Tile]:
        """
            Calculates the row and column number of the pos argument and returns the in-game tile object for that
            position. If there is no tile at the calculated position the function returns None
        """
        row: int = pos[0] // TILE_SIZE
        col: int = pos[1] // TILE_SIZE

        return self.tile_map.get((row, col), None)

    def get_neighbours(self, tile: Tile, directions: List[Tuple[int, int]]):
        """
          Returns immediately neighbouring tiles of the "tile" argument, for the directions
          listed in the "directions" argument if the neighbour tile exist on the map.
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
            Returns immediately neighbouring tiles in the cartesian directions of the "tile" argument.
            If the neighbour tile exist on the map.
        """

        # Cartesian directions only NO DIAGONALS
        directions: List[Tuple[int, int]] = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        return self.get_neighbours(tile, directions)

    def get_all_neighbours(self, tile: Tile) -> Optional[List[Tile]]:
        """
            Returns all immediately neighbouring tiles of the "tile" argument (four cardinal directions
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
        An Enemy object is alive if it is a member of the obstacle_sprites group and it's status instance variable is
        NOT set to "dead".
        """
        enemies: List[Enemy] = []
        for sprite in self.obstacle_sprites:
            if type(sprite) == Enemy:
                enemy: Enemy = sprite
                if enemy.is_alive():
                    enemies.append(enemy)

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
            path towards the player until either the player lies within the circle of attack or a path to the enemy
            cannot be found.
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
        """
        Releases dead objects of type LivingEntity to their corresponding object pools (via the object pool handler).
        after a time period defined in settings.py has elapsed.
        """
        def garbage_collection_countdown_time_elapsed(entity: LivingEntity) -> bool:
            current_time: int = pygame.time.get_ticks()
            if entity.time_of_death:
                return current_time - entity.time_of_death >= DEAD_OBJECT_CLEARANCE_COUNTDOWN_TIME
            return False

        for sprite in self.obstacle_sprites:
            if isinstance(sprite, LivingEntity) and garbage_collection_countdown_time_elapsed(sprite):
                entity: LivingEntity = sprite
                entity.kill()
                self.object_pool_handler.release(entity)

    def fade_consumed_object_entities(self) -> None:
        """
        Checks to see if consumable objects of type ObjectEntity have been consumed. i.e. their "has_object_been_used"
        instance attribute is set to True. If True the alpha value (transparency) is reduced by a rate defined
        in settings.py until the object is transparent (alpha value = 0). Once the object transparent it is removed from
        all the level groups (i.e. no longer intractable or rendered to screen) and sent to it's corresponding object
        pool (via the object pool handler).
        """

        def reduce_object_transparency(object_entity: ObjectEntity) -> None:
            reduced_alpha_value: float = object_entity.image.get_alpha() - OBJECT_ENTITY_ALPHA_VALUE_FADE_RATE if \
                object_entity.image.get_alpha() - OBJECT_ENTITY_ALPHA_VALUE_FADE_RATE > 0 else 0

            object_entity.image.set_alpha(reduced_alpha_value)

        def is_visible(object_entity: ObjectEntity) -> bool:
            return object_entity.image.get_alpha() > 0

        def has_been_consumed(object_entity: ObjectEntity) -> bool:
            return object_entity.has_object_been_used

        def de_spawn_consumed_object(entity: ObjectEntity) -> None:
            # remove from groups on the level
            entity.kill()
            self.object_pool_handler.release(entity)

        def object_still_active(entity: ObjectEntity) -> bool:
            return self.object_pool_handler.is_in_use(entity)

        for obj in self.visible_sprites:
            if isinstance(obj, ObjectEntity):
                if has_been_consumed(obj):
                    if is_visible(obj):
                        reduce_object_transparency(obj)
                    elif object_still_active(obj):
                        de_spawn_consumed_object(obj)

    def run(self) -> None:
        try:
            self.visible_sprites.custom_draw(self.player)
            if self.player.is_dead():
                self.level_handler.event_handler.set_game_over_screen()
        except Exception as e:
            print(e)

        self.visible_sprites.update()

        # Debugging
        try:
            enemy_sprite = [x for x in self.visible_sprites if type(x) == Enemy][0]
            # debug(f"enemy pool {self.enemy_object_pool.free}")
            debug(f"player health {self.player.health_points}, enemy_status {enemy_sprite.status}")
            # print(id(self.player))
            # debug(
                # f"object pool in use: {self.object_pool_handler.current_object_pool.in_use}, free: {self.object_pool_handler.current_object_pool.free}")

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
        floor_tiles: List[Tile] = [sprite for sprite in self.sprites() if not isinstance(sprite, LivingEntity) and
                                   (hasattr(sprite, "tiled_layer") and sprite.tiled_layer in ["Ground", "Carpet",
                                                                                              "Shadows"])]

        non_floor_tiles: List[pygame.sprite.Sprite] = [sprite for sprite in self.sprites() if
                                                       isinstance(sprite, AbstractEntity)
                                                       or
                                                       (hasattr(sprite, "tiled_layer") and sprite.tiled_layer not in [
                                                           "Ground", "Carpet", "Shadows"])]

        draw_floor_tiles(floor_tiles)
        draw_non_floor_tiles(non_floor_tiles)

    def regular_draw(self) -> None:
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
