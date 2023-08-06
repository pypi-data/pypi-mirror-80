# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volga']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'volga',
    'version': '0.1.2',
    'description': 'A python framework for deserialization',
    'long_description': "# volga &emsp; [![license]][license-file] [![release]][releases] [![python-version]][pypi] [![open-issues]][issues] [![last-commit]][commits] ![stars]\n\n\n[license]: https://img.shields.io/github/license/yefrig/volga\n[license-file]: https://github.com/yefrig/volga/blob/master/LICENSE\n\n[release]: https://img.shields.io/github/v/release/yefrig/volga?include_prereleases&sort=semver\n[releases]: https://github.com/yefrig/volga/releases\n\n[python-version]: https://img.shields.io/pypi/pyversions/volga\n[pypi]: https://pypi.org/project/volga/\n\n[open-issues]: https://img.shields.io/github/issues/yefrig/volga\n[issues]: https://github.com/yefrig/volga/issues\n\n[last-commit]: https://img.shields.io/github/last-commit/yefrig/volga\n[commits]: https://github.com/yefrig/volga/commits\n\n[stars]: https://img.shields.io/github/stars/yefrig/volga?style=social\n\n\n\n\n**volga is a framework for *de*serializing Python data structures.**\n\n---\n\nvolga will allow you to *flow* your data into any format that you'd like.\n\nExample:\n```python3\n  import volga-json\n  \n  @Deserealize\n  def class User():\n    name: Annotated<str, volga-json.exclude('yefri')>\n    age: int\n  \n  \n  # ...\n  \n  deserealized = volga-json.from_string(json_string)\n```\n\n## Team Members\n\n- Yefri Gaitan [@yefrig](https://github.com/yefrig)\n\n - Ecenaz (Jen) Ozmen [@eozmen410](https://github.com/eozmen410)\n",
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
