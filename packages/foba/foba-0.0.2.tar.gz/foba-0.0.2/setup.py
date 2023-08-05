# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['foba',
 'foba.dicts',
 'foba.dicts.dict_numbers',
 'foba.dicts.dict_strings',
 'foba.matrices',
 'foba.matrices.matrices_numbers',
 'foba.matrices.matrices_strings',
 'foba.objects',
 'foba.objects.point',
 'foba.tabulars',
 'foba.tabulars.crostabs',
 'foba.tabulars.tables',
 'foba.utils',
 'foba.utils.flops',
 'foba.utils.flops.dict_collection',
 'foba.utils.flops.vector_collection',
 'foba.utils.foo_dict',
 'foba.vectors',
 'foba.vectors.vector_strings',
 'foba.vectors.vector_strings.utils']

package_data = \
{'': ['*']}

install_requires = \
['veho>=0.0.4', 'way>=0.0.1']

setup_kwargs = {
    'name': 'foba',
    'version': '0.0.2',
    'description': 'placeholder sample objects for test',
    'long_description': '# foba\n##### placeholder sample objects for test\n\n### Usage\n```python\nfrom foba.dicts import pastas\n\nprint(pastas)\n```',
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydget/foba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
