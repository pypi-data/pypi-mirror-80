# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['debauto', 'debauto.bancos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'debauto',
    'version': '0.2.3',
    'description': 'Criação de remessas de débito automático no formato CNAB 150 da Febraban.',
    'long_description': None,
    'author': 'Flavio Milan',
    'author_email': 'oflaviomilan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
