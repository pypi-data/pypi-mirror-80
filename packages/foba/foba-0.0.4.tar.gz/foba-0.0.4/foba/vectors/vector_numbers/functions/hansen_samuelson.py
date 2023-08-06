from dataclasses import dataclass
from random import randint, uniform

GOV_EXPENDITURE = 100
CONSUMPTION = 50
INVESTMENT = 100
CONSUMPTION_MARGINAL_PROPENSITY = 0.28
INVESTMENT_MULTIPLIER = 5


@dataclass
class Economy:
    g: float = GOV_EXPENDITURE
    c: float = CONSUMPTION
    i: float = INVESTMENT
    a: float = CONSUMPTION_MARGINAL_PROPENSITY
    b: float = INVESTMENT_MULTIPLIER

    @property
    def y(self):
        return self.g + self.c + self.i

    def next(self):
        k = self.c
        self.c = self.a * self.y
        self.i = self.b * (self.c - k)
        return self


def hansen_samuelson_generator(econ: Economy):
    yield econ
    while True: yield econ.next()


def hansen_samuelson(hi: int, econ: Economy = None, d: int = 2):
    if econ is None:
        cb = randint(0, 3)
        ib = randint(1, 6)
        g = int((cb + ib) / 3) * 50
        c = cb * 50
        i = ib * 50
        a = uniform(0.15, 0.50)
        b = uniform(3.0, 8.0)
        econ = Economy(g, c, i, a, b)
    return [round(econ.y, d)] + \
           [round(econ.next().y, d) for _ in range(hi - 1)]
