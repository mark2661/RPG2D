import pygame
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
        self.tmx_data = load_pygame(map_path)

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()
        self.spawn_points = pygame.sprite.Group()

        # initialise map
        self.create_map()

        # set player
        self.player = player

    def create_map(self):
        """ This function creates individual tile objects for each tile in the .tmx file assigned to self.tmx_data
            and adds them to a pygame sprite group
        """
        pathable_tiles = list(self.tmx_data.get_layer_by_name("Pathing").tiles())

        def create_tile_objects():
            for layer in self.tmx_data.visible_layers:
                if hasattr(layer, "data"):
                    for x, y, surf in layer.tiles():
                        position = (x * TILE_SIZE, y * TILE_SIZE)
                        Tile(position, surf, [self.visible_sprites], layer.name)

        def create_collidable_objects():
            collidable_objects = self.tmx_data.get_layer_by_name("Collision_Objects")
            for collidable_object in collidable_objects:
                position = (collidable_object.x, collidable_object.y)
                size = (collidable_object.width, collidable_object.height)
                HitBox(position, size, [self.obstacle_sprites])

        def create_transition_objects():
            transition_objects = self.tmx_data.get_layer_by_name("Transition_Objects")
            for transition_object in transition_objects:
                position = (transition_object.x, transition_object.y)
                size = (transition_object.width, transition_object.height)
                TransitionBox(position, size, [self.transition_sprites], transition_object.transition_code)

        def create_spawn_point_objects():
            spawn_point_objects = self.tmx_data.get_layer_by_name("Spawn_Points")
            for spawn_point in spawn_point_objects:
                position = (spawn_point.x, spawn_point.y)
                SpawnPoint(position, [self.spawn_points], spawn_point.id)

        def create_enemies():
            enemy_spawn_position = ((self.display_surface.get_width() // 2)+500, (self.display_surface.get_height() // 2)+25)
            Enemy(enemy_spawn_position, ENEMY_IMAGES_FILE_PATH, [self.visible_sprites, self.obstacle_sprites],
                  self.obstacle_sprites)

        def is_pathable_tile(tile_top_left_pos: tuple[float, float]) -> bool:
            for index, pathable_tile in enumerate(pathable_tiles):
                pathable_tile_x, pathable_tile_y = pathable_tile
                if pathable_tile_x == tile_top_left_pos[0] and pathable_tile_y == tile_top_left_pos[1]:
                    pathable_tiles.pop(index)
                    return True

            return False

        create_tile_objects()
        create_collidable_objects()
        create_transition_objects()
        create_spawn_point_objects()
        create_enemies()

    def get_level_groups(self) -> list[pygame.sprite.Group]:
        return [self.visible_sprites, self.obstacle_sprites, self.transition_sprites, self.spawn_points]

    def set_player(self, player: Player):
        self.player = player

    def run(self):
        try:
            self.visible_sprites.custom_draw(self.player)
        except Exception as e:
            print(e)

        self.visible_sprites.update()
        debug(self.player.rect.center)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width, self.half_height = self.display_surface.get_width() // 2, self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Player):
        def draw_floor_tiles(tiles: list[pygame.sprite.Sprite]):
            # draw floor tiles before non-floor tiles (painters algorithm)
            for tile in tiles:
                offset = tile.rect.topleft - self.offset
                self.display_surface.blit(tile.image, offset)

        def draw_non_floor_tiles(tiles: list[pygame.sprite.Sprite]):
            # draw non-floor tiles on top of floor tiles using Y-sort algorithm
            for tile in sorted(tiles, key=lambda tile: tile.rect.centery):
                offset = tile.rect.topleft - self.offset
                self.display_surface.blit(tile.image, offset)

        # offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # separate floor tiles and non-floor tiles
        floor_tiles = [sprite for sprite in self.sprites() if not isinstance(sprite, Entity) and
                       sprite.tiled_layer in ["Ground", "Carpet", "Shadows"]]

        non_floor_tiles = [sprite for sprite in self.sprites() if isinstance(sprite, Entity) or
                           sprite.tiled_layer not in ["Ground", "Carpet", "Shadows"]]

        draw_floor_tiles(floor_tiles)
        draw_non_floor_tiles(non_floor_tiles)

    def regular_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
