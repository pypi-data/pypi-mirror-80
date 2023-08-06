# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volga']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'volga',
    'version': '0.1.1',
    'description': 'A python framework for deserialization',
    'long_description': '# coms4995-oss\nA semester-long project for coms4995 - Open Source Software Development\n\n\n## Ideas\n\n* My first idea was to create a program that can generate static websites from markdown composed files. It would also allow you to create your own template.\n\n* A python library for one functional feature such as lazy lists or immutable data structures. However, I found [PyFunctional](https://github.com/EntilZha/PyFunctional) and [Pyrsistent](https://pyrsistent.readthedocs.io/en/latest/), which seem to be very mature libraries. I might still try to implement something more specific.\n\nI would also love some suggestions if you have any. After looking at your streams library I was inspired to something cool with python.\n\n## Team Members\n\n- Yefri Gaitan [@yefrig](https://github.com/yefrig)\n\n - Ecenaz (Jen) Ozmen [@eozmen410](https://github.com/eozmen410)\n',
    'author': 'Yefri Gaitan',
    'author_email': 'yefrigaitan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yefrig/volga',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
