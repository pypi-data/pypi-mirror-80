import functools

class Binder:
    def default(self, func):
        return func

    def activate(self, func):
        return func

bind = Binder()