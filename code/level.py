import pygame
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Tile
from player import Player
from hitbox import HitBox
from transitionBox import TransitionBox
from spawnPoint import SpawnPoint
from debug import debug


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

        # initialise map
        self.create_map()

        self.player = player

    def create_map(self):
        """ This function creates individual tile objects for each tile in the .tmx file assigned to self.tmx_data
            and adds them to a pygame sprite group
        """
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    position = (x * TILE_SIZE, y * TILE_SIZE)
                    Tile(position, surf, [self.visible_sprites], layer.name)

        # create hitbox objects for collidable tiles
        collidable_objects = self.tmx_data.get_layer_by_name("Collision_Objects")
        for collidable_object in collidable_objects:
            position = (collidable_object.x, collidable_object.y)
            size = (collidable_object.width, collidable_object.height)
            HitBox(position, size, [self.obstacle_sprites])

        # crate transition box objects to trigger level changes when collided with
        transition_objects = self.tmx_data.get_layer_by_name("Transition_Objects")
        for transition_object in transition_objects:
            position = (transition_object.x, transition_object.y)
            size = (transition_object.width, transition_object.height)
            # currently passes spawn point as none - need to fix this
            TransitionBox(position, size, [self.transition_sprites], transition_object.transition_code)

        # create hit boxes for spawn points
        spawn_point_objects = self.tmx_data.get_layer_by_name("Spawn_Points")
        for spawn_point in spawn_point_objects:
            position = (spawn_point.x, spawn_point.y)
            SpawnPoint(position, [self.transition_sprites], spawn_point.id)

    def get_level_groups(self):
        return [self.visible_sprites, self.obstacle_sprites, self.transition_sprites]

    def set_player(self, player: Player):
        self.player = player

    def run(self):
        try:
            self.visible_sprites.custom_draw(self.player)
        except Exception as e:
            print(e)

        self.visible_sprites.update()
        debug(self.player.rect.center)
        # debug(pygame.mouse.get_pos())


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width, self.half_height = self.display_surface.get_width() // 2, self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Player):

        # offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # separate ground tiles and non-ground tiles
        floor_tiles = [sprite for sprite in self.sprites() if type(sprite) != Player and
                       sprite.tiled_layer in ["Ground", "Carpet", "Shadows"]]

        non_floor_tiles = [sprite for sprite in self.sprites() if type(sprite) == Player or
                           sprite.tiled_layer not in ["Ground", "Carpet", "Shadows"]]

        # draw floor tiles before non-floor tiles (painters algorithm)
        for floor_tile in floor_tiles:
            offset = floor_tile.rect.topleft - self.offset
            self.display_surface.blit(floor_tile.image, offset)

        # draw non-floor tiles on top of floor tiles
        # draw tiles using Y-sort algorithm
        for non_floor_tile in sorted(non_floor_tiles, key=lambda tile: tile.rect.centery):
            offset = non_floor_tile.rect.topleft - self.offset
            self.display_surface.blit(non_floor_tile.image, offset)
