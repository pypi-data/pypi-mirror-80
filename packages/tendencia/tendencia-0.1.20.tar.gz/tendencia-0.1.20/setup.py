# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tendencia']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tendencia = tendencia.cli:cli']}

setup_kwargs = {
    'name': 'tendencia',
    'version': '0.1.20',
    'description': '',
    'long_description': None,
    'author': 'chenn',
    'author_email': 'chenn@gisuni.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
