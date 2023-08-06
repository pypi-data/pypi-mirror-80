# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syngle']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'syngle',
    'version': '0.1.1',
    'description': 'Simple package implementing the Singleton pattern as a mixin class.',
    'long_description': '# Syngle\n\n\n[![pypi](https://img.shields.io/pypi/v/syngle.svg)](https://pypi.python.org/pypi/syngle) [![license](https://img.shields.io/github/license/valentincalomme/syngle.svg)](https://github.com/valentincalomme/syngle/blob/master/LICENSE)\n\n <!-- [![downloads](https://img.shields.io/pypi/dm/syngle.svg)](https://pypistats.org/packages/syngle) -->\n---\n\n**Documentation**: <a href="https://valentincalomme.github.io/syngle/" target="_blank">https://valentincalomme.github.io/syngle/</a>\n\n**Source Code**: <a href="https://github.com/ValentinCalomme/syngle/" target="_blank">https://github.com/ValentinCalomme/syngle/</a>\n\n---\n\n## Table of Contents\n\n  - [About](#about)\n  - [Installation](#installation)\n  - [Usage](#usage)\n\n## About\n\nSimple package implementing the Singleton pattern as a mixin class.\n\n## Installation\n\nSimply pip install the package!\n\n```\npip install syngle\n```\n\nThe package only has Python as a dependency to remain. It was developed for Python 3.8+ and has not been tested for prior versions.\n\n## Usage\n\nSimply import the Singleton class and make your classess extend it.\n\n```python\nfrom syngle import Singleton\n\nclass MyClass(Singleton):\n\n    pass\n\nmyclass1 = MyClass()\nmyclass2 = MyClass()\n\nassert myclass1 is myclass2\n```\n',
    'author': 'Valentin Calomme',
    'author_email': 'dev@valentincalomme.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://valentincalomme.github.io/syngle/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
