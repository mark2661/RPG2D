

class Observable:
    def __init__(self):
        self.observers = []

    def add(self, new_observer: Observer):
        self.observers.append(new_observer)

    def remove(self, observer_to_delete: Observer):
        for index, observer in enumerate(self.observers):
            if id(observer) == id(observer_to_delete):
                self.observers.pop(index)

    def notify(self):
        for observer in self.observers:
            observer.update()
