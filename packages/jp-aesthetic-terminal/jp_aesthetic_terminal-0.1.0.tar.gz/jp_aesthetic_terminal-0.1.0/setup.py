# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jp_aesthetic_terminal']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.8.0,<4.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['jp-aesthetic-terminal = '
                     'jp_aesthetic_terminal.console:main']}

setup_kwargs = {
    'name': 'jp-aesthetic-terminal',
    'version': '0.1.0',
    'description': 'Program for displaying Random Japanese Text in the terminal',
    'long_description': '[![Tests](https://github.com/ankhoudary12/jp-aesthetic-terminal/workflows/Tests/badge.svg)](https://github.com/ankhoudary12/jp-aesthetic-terminal/actions?workflow=Tests)\n\n[![PyPI](https://img.shields.io/pypi/v/jp-aesthetic-terminal.svg)](https://pypi.org/project/jp-aesthetic-terminal/)\n\n# jp-aesthetic-terminal\n',
    'author': 'Anthony Khoudary',
    'author_email': 'ankhoudary12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ankhoudary12/jp-aesthetic-terminal',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
