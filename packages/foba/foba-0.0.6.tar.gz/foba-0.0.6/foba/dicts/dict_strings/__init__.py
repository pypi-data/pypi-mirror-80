from types import MethodType

from .car_plants import car_plants
from .film_actors import film_actors
from .film_actresses import film_actresses
from .film_directors import film_directors
from .military_robots import military_robots
from .movie_quotes import movie_quotes
from .pastas import pastas
from .softwoods import softwoods
from ...utils import FooDict
from ...utils.flops.dict_collection import flop_shuffle

dict_collection = FooDict({
    'CarPlants': car_plants,
    'FilmActors': film_actors,
    'FilmActresses': film_actresses,
    'FilmDirectors': film_directors,
    'MilitaryRobots': military_robots,
    'MovieQuotes': movie_quotes,
    'Pastas': pastas,
    'Softwoods': softwoods,
})

dict_collection.flop_shuffle = MethodType(flop_shuffle, dict_collection)
