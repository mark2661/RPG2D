from singleton import Singleton
from typing import List, TYPE_CHECKING
from enemy import Enemy
from settings import *
from enemyFactory import EnemyFactory
from objectPool import ObjectPool

if TYPE_CHECKING:
    from level import Level
    from spawnPoint import SpawnPoint


class EnemyObjectPool(ObjectPool):

    def __init__(self) -> None:
        super().__init__()
        self.free: List[Enemy] = []
        self.in_use: List[Enemy] = []
        self.enemy_factory: EnemyFactory = EnemyFactory()

    def acquire(self, **kwargs) -> Enemy:
        try:
            level: "Level" = kwargs["level"]
        except KeyError:
            raise Exception(f"Error in {__name__} the following parameters are missing: level")

        if not self.free:
            try:
                spawnPoint: "SpawnPoint" = kwargs["spawnPoint"]
                new_enemy: Enemy = self.enemy_factory.create_enemy(enemy_spawn_point=spawnPoint, enemy_level=level)
                self.free.append(new_enemy)
            except KeyError:
                required_parameters: List[str] = ["spawnPoint: SpawnPoint", "level: Level"]
                missing_keys = [param for param in required_parameters if param not in kwargs]
                print(f"Error in {__name__} the following parameters are missing: {missing_keys}")

        enemy: Enemy = self.free.pop(0)
        enemy.reset(new_level=level)
        self.in_use.append(enemy)
        return enemy

    def release(self, enemy: Enemy) -> None:
        self.in_use.remove(enemy)
        self.free.append(enemy)

    def clear(self) -> None:
        self.free.clear()
        self.in_use.clear()


