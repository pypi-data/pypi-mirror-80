# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_insta']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.0.2,<7.0.0']

entry_points = \
{'pytest11': ['insta = pytest_insta.plugin']}

setup_kwargs = {
    'name': 'pytest-insta',
    'version': '0.0.0',
    'description': 'A flexible and user-friendly snapshot testing plugin for pytest',
    'long_description': '# pytest-insta\n\n> A flexible and user-friendly snapshot testing plugin for pytest.\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/pytest-insta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
