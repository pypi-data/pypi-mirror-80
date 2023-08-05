# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywdrwetter']

package_data = \
{'': ['*']}

install_requires = \
['MechanicalSoup>=0.12.0,<0.13.0',
 'click>=7.1.2,<8.0.0',
 'pandas>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['wdrwetter = pywdrwetter.main:main']}

setup_kwargs = {
    'name': 'pywdrwetter',
    'version': '0.1.0',
    'description': 'A simple command line webscraper for the weather forecast on wdr.de',
    'long_description': None,
    'author': 'Markus Mohnen',
    'author_email': 'markus.mohnen@gmail.com',
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
