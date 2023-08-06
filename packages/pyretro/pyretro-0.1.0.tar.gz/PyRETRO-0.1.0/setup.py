# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyretro']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyretro',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Scott McCallum',
    'author_email': 'sm@intermine.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
