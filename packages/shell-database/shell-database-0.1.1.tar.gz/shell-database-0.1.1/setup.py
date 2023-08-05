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
    'version': '0.1.1',
    'description': 'A key value store for the shell',
    'long_description': '# Shell Database\n\n## Installation\n\nYou can install shell-database from `pypi.org`:\n```console\n> pip install shell_database\n```\n\n## Getting started\n\n### Adding a new key value pair\n```\n> shdb add name "John Doe"\n```\n\n### Adding a new key value pair with encryption\n\n```\n> shdb add password <your_password> --encrypt\n```\n\n### Getting the value of a key\n\n```console\n> shdb get name\nJohn Doe\n```\n\n### Decrypting and encrypted value\n\n```console\n> shdb get password\nb\'51b8684c4dc77da0979f1b647caa707c\'\n\n> shdb get password --decrypt\n<your_password>\n```\n\n### Integrating with other tools\n\n```console\n> shdb add az-rg azure-resource-group-123\n\n> az postgres db create --resource-group $(shdb get az-rg) --server-name server_name --name database\n```\n\n## License\n\nMIT License\n\n## Disclaimer\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
    'author': 'José Coelho',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jcoelho93/shell-database',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
