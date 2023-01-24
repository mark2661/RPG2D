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
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.transition_sprites = pygame.sprite.Group()

        self.create_map()

        # create player object
        player_spawn_position = tuple(map(lambda x: x//2, self.display_surface.get_size()))
        self.player = Player(player_spawn_position, TEST_PLAYER_IMAGE_FILE_PATH, [self.visible_sprites]) # change TEST_PLAYER_IMAGE_FILE_PATH at later data


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
        self.visible_sprites.draw(self.display_surface)