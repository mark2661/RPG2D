from singleton import Singleton
from typing import List, TYPE_CHECKING
from enemy import Enemy
from settings import *
from enemyFactory import EnemyFactory
from abstractObjectPool import AbstractObjectPool

if TYPE_CHECKING:
    from level import Level
    from spawnPoint import SpawnPoint


class EnemyObjectPool(metaclass=Singleton):

    def __init__(self) -> None:
        super().__init__()
        self.free: List[Enemy] = []
        self.in_use: List[Enemy] = []
        self.enemy_factory: EnemyFactory = EnemyFactory()

    def acquire(self, spawnPoint: "SpawnPoint", level: "Level") -> Enemy:
        if not self.free:
            new_enemy: Enemy = self.enemy_factory.create_enemy(enemy_spawn_point=spawnPoint, enemy_level=level)
            self.free.append(new_enemy)

        enemy: Enemy = self.free.pop(0)
        self.in_use.append(enemy)
        return enemy

    def release(self, enemy: Enemy) -> None:
        self.in_use.remove(enemy)
        enemy.reset()
        self.free.append(enemy)
