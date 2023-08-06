# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytm']

package_data = \
{'': ['*'], 'pytm': ['images/*', 'threatlib/*']}

install_requires = \
['pydal>=20200714.1,<20200714.2']

setup_kwargs = {
    'name': 'pytm',
    'version': '1.1.2',
    'description': 'A Pythonic framework for threat modeling',
    'long_description': None,
    'author': 'pytm Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
