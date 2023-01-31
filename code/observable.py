from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from observer import Observer


class Observable:
    def __init__(self):
        self.observers = []

    def observable_add(self, new_observer: "Observer"):
        self.observers.append(new_observer)

    def observable_remove(self, observer_to_delete: "Observer"):
        for index, observer in enumerate(self.observers):
            if id(observer) == id(observer_to_delete):
                self.observers.pop(index)

    def observable_notify(self):
        for observer in self.observers:
            observer.update()
