# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subito', 'subito.db', 'subito.operations']

package_data = \
{'': ['*']}

install_requires = \
['gql>=3.0.0-alpha.1,<4.0.0',
 'python-box>=5.1.1,<6.0.0',
 'tinydb>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'subito',
    'version': '0.1.1',
    'description': 'Quickly create stateless microservices based on GraphQL subscription messages.',
    'long_description': None,
    'author': 'Milos Grujic',
    'author_email': 'srbiotik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
