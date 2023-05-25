from typing import List, TYPE_CHECKING, Tuple
from settings import *
from healthObjectFactory import HealthObjectFactory
from objectPool import ObjectPool

if TYPE_CHECKING:
    from level import Level
    from spawnPoint import SpawnPoint
    from healthObject import HealthObject


class HealthObjectObjectPool(ObjectPool):

    def __init__(self) -> None:
        super().__init__()
        self.free: List["HealthObject"] = []
        self.in_use: List["HealthObject"] = []
        self.health_object_factory: HealthObjectFactory = HealthObjectFactory()

    def acquire(self, **kwargs) -> "HealthObject":
        if not self.free:
            try:
                position: Tuple[float, float] = kwargs["position"]
                level: "Level" = kwargs["level"]
                new_health_object: "HealthObject" = self.health_object_factory.create_full_health_object(
                                                    position=position, level=level)
                self.free.append(new_health_object)
            except KeyError:
                required_parameters: List[str] = ["position: Tuple[float, float]", "level: Level"]
                missing_keys = [param for param in required_parameters if param not in kwargs]
                print(f"Error in {__name__} the following parameters are missing: {missing_keys}")

        health_object: "HealthObject" = self.free.pop(0)
        self.in_use.append(health_object)
        return health_object

    def release(self, health_object: "HealthObject") -> None:
        self.in_use.remove(health_object)
        health_object.reset()
        self.free.append(health_object)

    def clear(self) -> None:
        self.free.clear()
        self.in_use.clear()
