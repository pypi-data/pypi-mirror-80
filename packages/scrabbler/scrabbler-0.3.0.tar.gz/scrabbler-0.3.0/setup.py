# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrabbler']

package_data = \
{'': ['*']}

install_requires = \
['string_algorithms>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['scrabbler = scrabbler.scrabbler:main']}

setup_kwargs = {
    'name': 'scrabbler',
    'version': '0.3.0',
    'description': 'Scrabbler.',
    'long_description': None,
    'author': 'Michal Hozza',
    'author_email': 'mhozza@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
