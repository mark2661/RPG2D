from abc import ABC, abstractclassmethod
from singleton import Singleton
from typing import List, TYPE_CHECKING, Dict, Set, Optional
from healthObject import HealthObject
from collections import defaultdict
from enemyObjectPool import EnemyObjectPool
from healthObjectObjectPool import HealthObjectObjectPool
from enemy import Enemy
from healthObject import HealthObject

if TYPE_CHECKING:
    from level import Level
    from objectPool import ObjectPool


class ObjectPoolHandler(metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.object_pools: dict[str, "ObjectPool"] = {
                                                        Enemy.__name__: EnemyObjectPool(),
                                                        HealthObject.__name__: HealthObjectObjectPool()
                                                     }
        self.current_object_pool: Optional["ObjectPool"] = None

    # hacky and bad implementation need to fix
    def set_current_object_pool(self, obj: object) -> None:
        try:
            self.current_object_pool = self.object_pools[obj.__name__]

        except:
            self.current_object_pool = self.object_pools[type(obj).__name__]

    def is_current_object_pool_correct(self, object_param: object) -> bool:
        correct_object_pools_mapping = {Enemy: EnemyObjectPool, HealthObject: HealthObjectObjectPool}
        # hacky and bad implementation need to fix
        current_object_pool: "ObjectPool" = correct_object_pools_mapping[[key for key in correct_object_pools_mapping if key in correct_object_pools_mapping or isinstance(object_param, key)][0]]
        # return self.current_object_pool == correct_object_pools_mapping[type(object_param)]
        return self.current_object_pool == current_object_pool

    def acquire(self, obj: object, **kwargs) -> object:
        if not self.is_current_object_pool_correct(obj):
            self.set_current_object_pool(obj)

        return self.current_object_pool.acquire(**kwargs)

    def release(self, *args) -> None:
        obj = args[0]
        if not self.is_current_object_pool_correct(obj):
            self.set_current_object_pool(obj)

        self.current_object_pool.release(obj)

    def is_in_use(self, *args) -> bool:
        obj = args[0]
        if not self.is_current_object_pool_correct(obj):
            self.set_current_object_pool(obj)

        return obj in self.current_object_pool.in_use

    def clear_all_object_pools(self) -> None:
        for object_pool in self.object_pools.values():
            object_pool.clear()

    def free_all_objects_in_all_object_pools(self) -> None:
        # print(self.free_all_objects_in_all_object_pools.__name__)
        for object_pool in self.object_pools.values():
            object_pool.release_all()



