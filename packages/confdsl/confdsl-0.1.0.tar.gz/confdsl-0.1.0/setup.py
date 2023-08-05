# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confdsl']

package_data = \
{'': ['*']}

install_requires = \
['pyhcl>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'confdsl',
    'version': '0.1.0',
    'description': 'wrapper to make reading config from various DSLs easy',
    'long_description': None,
    'author': 'Ayush',
    'author_email': 'ayushshanker@outlook.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
