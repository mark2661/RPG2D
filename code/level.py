import pygame
from pytmx.util_pygame import load_pygame
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self, map_path: str) -> None:
        # load map
        self.tmx_data = load_pygame(map_path)

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()

        self.create_map()

        # create player object
        player_spawn_position = tuple(map(lambda x: x // 2, self.display_surface.get_size()))
        self.player = Player(player_spawn_position, TEST_PLAYER_IMAGE_FILE_PATH,
                             [self.visible_sprites])  # change TEST_PLAYER_IMAGE_FILE_PATH at later data

    def create_map(self):
        """ This function creates individual tile objects for each tile in the .tmx file assigned to self.tmx_data
            and adds them to a pygame sprite group
        """
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    position = (x * TILE_SIZE, y * TILE_SIZE)
                    Tile(position, surf, [self.visible_sprites], layer.name)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


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
