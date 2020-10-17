class Environment:
    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    def get(self, name):
        result = self.store.get(name)
        if result is None and self.outer is not None:
            return self.outer.get(name)
        return result

    def set(self, name, val):
        self.store[name] = val
        return val
