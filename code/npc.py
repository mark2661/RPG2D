import pygame
from settings import *
from livingentity import LivingEntity
from typing import Optional, Union, List, TYPE_CHECKING, Tuple, Dict, Callable
from a_star import a_star

if TYPE_CHECKING:
    from tile import Tile
    from level import Level, YSortCameraGroup
    from player import Player
    from spawnPoint import SpawnPoint


class NPC(LivingEntity):
    """
    NPC Class serves as a blueprint for creating NPCs in a game, providing fundamental attributes and methods for
    movement, collision detection, rendering, and interaction. Subclasses can inherit from this base class to extend its
    functionality and customize the behavior of specific NPC types.
    """
    def __init__(self, spawn_point: "SpawnPoint", asset_image_root_dir_path: str, level: "Level",
                 groups: List[Union["YSortCameraGroup", pygame.sprite.Sprite]],
                 obstacle_sprites: pygame.sprite.Group) -> None:
        super().__init__(spawn_point, asset_image_root_dir_path, groups, obstacle_sprites)

        # store the level object in associated with the instance
        # self.level: Level = level

    def update_status(self) -> None:
        """
        updates the entities status variable which is used to select the correct image to be displayed for the
        current position
        """
        pass

    def reset(self, *args, **kwargs) -> None:
        """
           Resets the NPC's attributes
        """
        pass

    def check_if_npc_should_be_dead(self) -> None:
        """
        Checks if the NPC's health has dropped to or below zero and sets the NPC's status attribute to "dead"
        if it's still alive.
        """

        def kill_npc() -> None:
            """
            Sets the NPC's status to dead, changes the animation mode to "dead," and resets the frame index for the
            death animation
            """
            self.status = "dead"
            # recorded time of death for de-spawn algorithm
            self.time_of_death = pygame.time.get_ticks()
            # set animation mode (in parent class) to "dead"
            self.animation_mode = self.animation_modes["dead"]
            self.frame_index = 0  # reset the frame index so the death animation starts from the first frame.

        if "dead" not in self.status and self.health_points <= 0:
            kill_npc()

    # Override parent method
    def update(self) -> None:
        self.check_if_npc_should_be_dead()
        # print(f"in NPC: {self.is_dead()}")
        super().update()
