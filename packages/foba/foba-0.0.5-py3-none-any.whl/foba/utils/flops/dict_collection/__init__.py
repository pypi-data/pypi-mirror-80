import random


def flop_shuffle(self, length=3):
    k, lex = random.choice(list(self.items()))
    length = min(len(lex), length)
    return k, dict(random.sample(list(lex.items()), length))
