# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py591']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2,<2.0.0',
 'Pillow>=7.2.0,<8.0.0',
 'beautifulsoup4>=4.9.0,<5.0.0',
 'pytesseract>=0.3.5,<0.4.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'py591',
    'version': '0.0.3',
    'description': 'Parser and parsing API service for 591 Housing Rental service',
    'long_description': None,
    'author': 'Frank Chang',
    'author_email': 'frank@csie.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
