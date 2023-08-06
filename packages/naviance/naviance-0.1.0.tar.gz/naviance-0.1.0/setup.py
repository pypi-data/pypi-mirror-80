# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['naviance']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.2,<5.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'naviance',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Charlie Bini',
    'author_email': 'cbini87@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
