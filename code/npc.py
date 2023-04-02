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


class NPC(Entity):
    def __init__(self, spawn_point: "SpawnPoint", asset_image_root_dir_path: str, level: "Level",
                 groups: List[Union["YSortCameraGroup", pygame.sprite.Sprite]],
                 obstacle_sprites: pygame.sprite.Group) -> None:

        super().__init__(spawn_point, asset_image_root_dir_path, groups, obstacle_sprites)

        # store the level object in associated with the instance
        self.level: Level = level

    def update_status(self) -> None:
        """
        updates the entities status variable which is used to select the correct image to be displayed for the
        current position
        """
        pass

    def kill_npc(self) -> None:
        """
        Sets the Entities status to dead, if the health has dropped to zero or below if the Entity
        is not marked as dead, also removes Entity from its levels obstacle groups. This prevents the player from
        interacting with it any longer, e.g. collisions, attacks, e.t.c.
        """
        if "dead" not in self.status and self.health_points <= 0:
            self.status = "dead"
            # remove from obstacle groups. DON'T remove from visible_sprite group so it is still drawn on screen
            self.level.obstacle_sprites.remove(self)
    
    # Override parent method
    def update(self) -> None:
        if not self.is_dead():
            self.kill_npc()
            # print(f"in NPC: {self.is_dead()}")
            super().update()

