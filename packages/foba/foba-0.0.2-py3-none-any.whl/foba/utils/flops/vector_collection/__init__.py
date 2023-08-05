import random


def flop_shuffle(self, length=3):
    k, vec = random.choice(list(self.items()))
    length = min(len(vec), length)
    return k, random.sample(vec, length)
