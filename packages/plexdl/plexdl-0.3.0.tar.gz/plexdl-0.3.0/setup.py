# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plexdl']

package_data = \
{'': ['*']}

install_requires = \
['PlexAPI>=4.0.0,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'humanfriendly>=8.2,<9.0',
 'importlib_metadata>=1.6.1,<2.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['plexdl = plexdl.cli:main']}

setup_kwargs = {
    'name': 'plexdl',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Hoherd',
    'author_email': 'daniel.hoherd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
