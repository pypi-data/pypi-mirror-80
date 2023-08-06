from math import e, pi, sqrt
from random import randint, sample

specials = {
    "PI": pi,
    "E": e,
    "SQR_2": sqrt(2),
    "SQR_3": sqrt(3),
    "SQR_5": sqrt(5),
    "GOLDEN": 1.61803398874989484820,
    "MP10_3": 10 / 3,
    "MP10_6": 10 / 6,
    "GRAVITY": 6.67430,
    "FEIGENBAUM": 4.669201609102990671853203821578,
    "GAUSS_STDEV_1": 68.2689492137,
    "GAUSS_STDEV_2": 95.4499736104,
    "GAUSS_STDEV_3": 99.7300203937,
    "LIGHT": 299792458,  # m/s**2
    "MOL": 6.02214076e+23,
    "LOSCHMIDT": 2.6867811e+25,
    "ABSOLUTE_ZERO": -273.15
}


def rand_float(): return 2 ** randint(1, 12) - 1


def absolute_mirror(size=5, d=3):
    size = 4 if size < 4 else size
    h, r = int(size / 2), size % 2
    positives = sample(list(specials.values()), h - 1)
    positives.append(rand_float())
    positives = [abs(x) for x in positives]
    positives.sort()
    negatives = [-x for x in positives]
    negatives.reverse()
    if (r): negatives.append(0)
    return [round(x, d) for x in (negatives + positives)]
