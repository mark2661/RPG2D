from typing import Tuple, List, TYPE_CHECKING
from healthObject import HealthObject

if TYPE_CHECKING:
    from level import Level


class HealthObjectFactory:
    def __init__(self):
        pass

    def create_health_object(self, position: Tuple[float, float], level: "Level", health: int):
        return HealthObject(position, level, health)

    def create_full_health_object(self, position: Tuple[float, float], level: "Level"):
        return self.create_health_object(position, level, health=100)