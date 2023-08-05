# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shell_database', 'shell_database.store']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'coveralls>=2.1.2,<3.0.0',
 'cryptography>=3.1,<4.0',
 'flake8>=3.8.3,<4.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'sqlitedict>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['shdb = shell_database.shdb:cli']}

setup_kwargs = {
    'name': 'shell-database',
    'version': '0.1.0',
    'description': 'A key value store for the shell',
    'long_description': None,
    'author': 'José Coelho',
    'author_email': 'camilocoelho93@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
