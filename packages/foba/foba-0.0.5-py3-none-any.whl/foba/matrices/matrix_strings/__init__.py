from foba.matrices.matrix_strings.CompanyBrandTypes import CompanyBrandTypes
from foba.matrices.matrix_strings.Countries import Countries
from foba.matrices.matrix_strings.IntegratedCultureFramework import IntegratedCultureFramework
from foba.matrices.matrix_strings.MarketingMovement import MarketingMovement
from foba.utils import FooDict

matrix_collection = FooDict({
    'CompanyBrandTypes': CompanyBrandTypes,
    'Countries': Countries,
    'IntegratedCultureFramework': IntegratedCultureFramework,
    'MarketingMovement': MarketingMovement,
})
