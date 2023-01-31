from observable import Observable


class Observer:
    def __init__(self, observable: Observable):
        self.observable = observable

    def update(self):
        pass
