# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syngle']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'syngle',
    'version': '0.1.0',
    'description': 'Simple package implementing the Singleton pattern as a mixin class.',
    'long_description': None,
    'author': 'Valentin Calomme',
    'author_email': 'dev@valentincalomme.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
