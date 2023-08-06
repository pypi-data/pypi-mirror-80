# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glortrou']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'glortrou',
    'version': '0.0.0',
    'description': 'An UDP hole-punching server, client and broker based on AsyncIO',
    'long_description': '# glortrou\n\n***glortrou*** is an UDP hole-punching library based on Asyncio.\n\n## WIP\n',
    'author': 'Frank Chang',
    'author_email': 'frank@csie.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frankurcrazy/glortrou',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
