# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['metaloaders']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser']

setup_kwargs = {
    'name': 'metaloaders',
    'version': '20.9.2341636',
    'description': 'A JSON Loader with column and line numbers.',
    'long_description': '# Meta-JSON\n\n[![Release](\nhttps://img.shields.io/pypi/v/metaloaders?color=success&label=Release&style=flat-square)](\nhttps://pypi.org/project/metaloaders)\n[![Documentation](\nhttps://img.shields.io/badge/Documentation-click_here!-success?style=flat-square)](\nhttps://kamadorueda.github.io/metaloaders/)\n[![Downloads](\nhttps://img.shields.io/pypi/dm/metaloaders?label=Downloads&style=flat-square)](\nhttps://pypi.org/project/metaloaders)\n[![Status](\nhttps://img.shields.io/pypi/status/metaloaders?label=Status&style=flat-square)](\nhttps://pypi.org/project/metaloaders)\n[![Coverage](\nhttps://img.shields.io/badge/Coverage-100%25-success?style=flat-square)](\nhttps://kamadorueda.github.io/metaloaders/)\n[![License](\nhttps://img.shields.io/pypi/l/metaloaders?color=success&label=License&style=flat-square)](\nhttps://github.com/kamadorueda/metaloaders/blob/latest/LICENSE.md)\n',
    'author': 'Kevin Amado',
    'author_email': 'kamadorueda@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kamadorueda.github.io/metaloaders',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
