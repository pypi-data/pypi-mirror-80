# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plenty_api']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=21.4.0,<22.0.0', 'pandas>=1.1.2,<2.0.0', 'simplejson>=3.17.2,<4.0.0']

setup_kwargs = {
    'name': 'plenty-api',
    'version': '0.1',
    'description': 'Interface for the PlentyMarkets API.',
    'long_description': '# Overview\n\nInterface for the PlentyMarkets API.\n\n# Setup\n\n## Requirements\n\n* Python 3.7.8+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install python_plenty_api\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add python_plenty_api\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import plenty_api\n>>> plenty_api.__version__\n```\n',
    'author': 'Sebastian Fricke',
    'author_email': 'sebastian.fricke.linux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/plenty_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
