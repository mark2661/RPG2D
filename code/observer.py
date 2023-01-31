from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from observable import Observable


class Observer:
    def __init__(self, observable: "Observable"):
        self.observable = observable

    def observer_update(self):
        pass
