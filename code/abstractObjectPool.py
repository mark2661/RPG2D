from abc import ABC, abstractclassmethod
from singleton import Singleton
from typing import List, TYPE_CHECKING
from healthObject import HealthObject

if TYPE_CHECKING:
    from level import Level


class AbstractObjectPool(metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()
        # super(Singleton, self).__init__()
        # Singleton.__init__(self)
        # ABC.__init__(self)
        self.free: List[object] = []
        self.in_use: List[object] = []

    # @abstractclassmethod
    def acquire(self, *args) -> object:
        pass

    # @abstractclassmethod
    def release(self, *args) -> None:
        pass