import random
from types import MethodType

from foba.utils import FooDict
from foba.vectors.vector_numbers.functions import \
    absolute_mirror, \
    compound_interest, \
    fibonacci, \
    hansen_samuelson, \
    leonardo, \
    primes

vector_collection = FooDict({
    'absolute_mirror': absolute_mirror,
    'compound_interest': compound_interest,
    'fibonacci': fibonacci,
    'hansen_samuelson': hansen_samuelson,
    'leonardo': leonardo,
    'primes': primes,
})


def flop_shuffle(self, length=3):
    k, fn = random.choice(list(self.items()))
    return k, fn(length)


vector_collection.flop_shuffle = MethodType(flop_shuffle, vector_collection)
