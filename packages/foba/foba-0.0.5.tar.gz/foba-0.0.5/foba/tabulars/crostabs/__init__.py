from foba.tabulars.crostabs.AoEIIUnitsAttackByStages import AoEIIUnitsAttackByStages
from foba.tabulars.crostabs.AoEIIUnitsHpByStages import AoEIIUnitsHpByStages
from foba.tabulars.crostabs.AreaByCountry import AreaByCountry
from foba.tabulars.crostabs.BigMacAdjustedIndexes import BigMacAdjustedIndexes
from foba.tabulars.crostabs.CountryGDPByYear import CountryGDPByYear
from foba.tabulars.crostabs.FinancialAssetsToGDPByYear import FinancialAssetsToGDPByYear
from foba.tabulars.crostabs.MilitaryByCountry2019 import MilitaryByCountry2019
from foba.tabulars.crostabs.TeachersCountByYear import TeachersCountByYear
from foba.utils import FooDict

crostab_collection = FooDict({
    'AoEIIUnitsAttackByStages': AoEIIUnitsAttackByStages,
    'AoEIIUnitsHpByStages': AoEIIUnitsHpByStages,
    'AreaByCountry': AreaByCountry,
    'BigMacAdjustedIndexes': BigMacAdjustedIndexes,
    'CountryGDPByYear': CountryGDPByYear,
    'FinancialAssetsToGDPByYear': FinancialAssetsToGDPByYear,
    'MilitaryByCountry2019': MilitaryByCountry2019,
    'TeachersCountByYear': TeachersCountByYear,
})
