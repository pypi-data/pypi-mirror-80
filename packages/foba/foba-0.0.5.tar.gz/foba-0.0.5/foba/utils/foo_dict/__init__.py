import inspect
import random


class FooDict(dict):
    def __init__(self, seq=None, **kwargs):
        super().__init__(seq, **kwargs)

    def flop_shuffle(self, length=5):
        k, o = random.choice(list(self.items()))
        if inspect.isfunction(o): return k, o(length)
        return k, o
