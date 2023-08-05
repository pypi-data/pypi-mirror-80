from types import MethodType

from texting import DOT, SP

from foba.vectors.vector_strings.actors import actors
from foba.vectors.vector_strings.actresses import actresses
from foba.vectors.vector_strings.directors import directors
from ...dicts.dict_numbers import arm_sales, mega_cities, mortality_rates, power_cars, recessions
from ...dicts.dict_strings import car_plants, film_actors, film_actresses, film_directors, pastas
from ...utils import FooDict
from ...utils.flops.vector_collection import flop_shuffle


def brief_name(name):
    vec = name.split(SP)
    last = vec.pop()
    while last == 'Jr.':
        last = vec.pop() + last
    return DOT.join([x[0] for x in vec]) + DOT + last


vector_collection = FooDict({
    'actors': actors,
    'actresses': actresses,
    'directors': directors,
    'carPlants': list(car_plants),
    'actorBriefs': [brief_name(x) for x in film_actors.values()],
    'actressBriefs': [brief_name(x) for x in film_actresses.values()],
    'directorBriefs': [brief_name(x) for x in film_directors.values()],
    'pastas': list(pastas),
    'armDealers': list(arm_sales),
    'megaCities': list(mega_cities),
    'deathCauses': list(mortality_rates),
    'powerCars': list(power_cars),
    'recessionYears': list(recessions),
})

vector_collection.flop_shuffle = MethodType(flop_shuffle, vector_collection)
