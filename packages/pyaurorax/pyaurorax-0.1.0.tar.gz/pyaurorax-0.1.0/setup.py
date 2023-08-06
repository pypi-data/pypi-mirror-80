# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aurorax']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.3,<4.0.0', 'humanize>=2.6.0,<3.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'pyaurorax',
    'version': '0.1.0',
    'description': 'Python library for interacting with the AuroraX API',
    'long_description': None,
    'author': 'Darren Chaddock',
    'author_email': 'dchaddoc@ucalgary.ca',
    'maintainer': 'Darren Chaddock',
    'maintainer_email': 'dchaddoc@ucalgary.ca',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
