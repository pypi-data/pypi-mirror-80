import json

from foba.utils import FooDict

agriculture_forestry_fishing_va = json.load(open('AgricultureForestryFishingVA.json'))
arms_exports = json.load(open('ArmsExports.json'))
arms_imports = json.load(open('ArmsImports.json'))
big_mac_index = json.load(open('BigMacIndex.json'))
consumption_expenditure = json.load(open('ConsumptionExpenditure.json'))
gdp = json.load(open('Gdp.json'))
industry_va = json.load(open('IndustryVA.json'))
manufacturing_va = json.load(open('ManufacturingVA.json'))
market_cap_listed_domestic = json.load(open('MarketCapListedDomestic.json'))
military_expenditure = json.load(open('MilitaryExpenditure.json'))
population = json.load(open('Population.json'))
rural_population = json.load(open('RuralPopulation.json'))
stocks_traded_value = json.load(open('StocksTradedValue.json'))
urban_population = json.load(open('UrbanPopulation.json'))

dict_collection = FooDict({
    'AgricultureForestryFishingVA': agriculture_forestry_fishing_va,
    'ArmsExports': arms_exports,
    'ArmsImports': arms_imports,
    'BigMacIndex': big_mac_index,
    'ConsumptionExpenditure': consumption_expenditure,
    'Gdp': gdp,
    'IndustryVA': industry_va,
    'ManufacturingVA': manufacturing_va,
    'MarketCapListedDomestic': market_cap_listed_domestic,
    'MilitaryExpenditure': military_expenditure,
    'Population': population,
    'RuralPopulation': rural_population,
    'StocksTradedValue': stocks_traded_value,
    'UrbanPopulation': urban_population,
})
