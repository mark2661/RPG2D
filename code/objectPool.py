from abc import ABC, abstractmethod
from typing import List


class ObjectPool(ABC):
    def __init__(self):
        # super.__init__()
        self.free: List[object] = []
        self.in_use: List[object] = []

    @abstractmethod
    def acquire(self, *args, **kwargs):
        pass

    @abstractmethod
    def release(self, *args, **kwargs):
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
