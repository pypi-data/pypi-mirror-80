from types import MethodType

from .arm_sales import arm_sales
from .brent_prices import brent_prices
from .mega_cities import mega_cities
from .mortality_rates import mortality_rates
from .power_cars import power_cars
from .recessions import recessions
from ...utils import FooDict
from ...utils.flops.dict_collection import flop_shuffle

dict_collection = FooDict({
    'ArmSales': arm_sales,
    'BrentPrices': brent_prices,
    'MegaCities': mega_cities,
    'MortalityRates': mortality_rates,
    'PowerCars': power_cars,
    'Recessions': recessions,
})

dict_collection.flop_shuffle = MethodType(flop_shuffle, dict_collection)
