import os

import pygame.display

from settings import *
from level import Level
from player import Player


class LevelHandler:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.levels = {
                        0: Level(os.path.join(MAPS_FILE_PATH, "0.tmx")),
                        1: Level(os.path.join(MAPS_FILE_PATH, "1.tmx"))
                      } # need to automate

        # initialise current level to the starting level
        self.current_level_code = 0
        self.current_level = self.levels[self.current_level_code]

        # get the pygame group member objects of the current level
        self.visible_sprites_group, self.obstacle_sprites_group,\
            self.transition_sprites_group, self.spawn_points_group = self.current_level.get_level_groups()

        # create the player instance that will be passed between levels
        player_spawn_position = tuple(map(lambda x: x // 2, self.display_surface.get_size()))
        player_spawn_image_file_path = os.path.join(PLAYER_IMAGES_FILE_PATH, "down_idle", "down_idle_1.png")
        self.player = Player(player_spawn_position, player_spawn_image_file_path, [self.visible_sprites_group],
                             self.obstacle_sprites_group, self.transition_sprites_group, self.spawn_points_group,
                             self.current_level_code)

        # pass the player instance to the current level
        self.current_level.set_player(self.player)

    def transition(self):
        # if player has collided with a transition object
        if self.current_level_code != self.player.get_current_level_code():
            # update current level code
            self.current_level_code = self.player.get_current_level_code()
            # change current level
            self.current_level = self.levels[self.current_level_code]

            # update group attributes
            self.update_groups()

            # move player instance to new level
            self.current_level.set_player(self.player)
            # update player object groups
            self.player.set_groups(self.current_level.get_level_groups())
            # draw new map
            self.current_level.visible_sprites.regular_draw()
            # set new player pos
            self.player.rect.center = self.get_spawn_point(self.player.next_level_spawn_id).rect.center

    def update_groups(self):
        # get the pygame group member objects of the current level
        self.visible_sprites_group, self.obstacle_sprites_group, \
            self.transition_sprites_group, self.spawn_points_group = self.current_level.get_level_groups()

    def get_spawn_point(self, spawn_point_id):
        for sprite in self.spawn_points_group:
            if sprite.get_spawn_point_id() == spawn_point_id:
                return sprite

        return None
    def run(self):
        self.current_level.run()
        self.transition()


