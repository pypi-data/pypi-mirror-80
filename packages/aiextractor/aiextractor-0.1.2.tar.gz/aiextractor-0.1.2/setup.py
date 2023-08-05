# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiextractor']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'aiextractor',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@mjaquier.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
