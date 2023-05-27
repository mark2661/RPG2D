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

    def release_all(self) -> None:
        self.free += self.in_use
        self.in_use.clear()
        # print(f" free: {self.free}, in_use: {self.in_use}")
