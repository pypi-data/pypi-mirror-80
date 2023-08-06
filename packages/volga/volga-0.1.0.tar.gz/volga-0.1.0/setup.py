# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volga']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'volga',
    'version': '0.1.0',
    'description': 'A python framework for deserialization',
    'long_description': None,
    'author': 'Yefri Gaitan',
    'author_email': 'yefrigaitan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
