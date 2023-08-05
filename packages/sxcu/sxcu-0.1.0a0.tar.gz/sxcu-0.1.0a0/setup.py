# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sxcu']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.0.2,<7.0.0', 'requests>=2.24.0,<3.0.0', 'tox>=3.20.0,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

setup_kwargs = {
    'name': 'sxcu',
    'version': '0.1.0a0',
    'description': 'Python API wraper for sxcu.net',
    'long_description': '[![PyPI Version](https://img.shields.io/pypi/v/sxcu)](https://pypi.org/project/scxu/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/scxu)](https://pypi.org/project/scxu/)\n[![Python Wheel](https://img.shields.io/pypi/wheel/scxu)](https://pypi.org/project/scxu/)\n[![License](https://img.shields.io/badge/License-Apache2.0-green.svg)](https://opensource.org/licenses/Apache-2.0)\n[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Code Quality: flake8](https://img.shields.io/badge/code%20quality-flake8-000000.svg)](https://gitlab.com/pycqa/flake8)\n\n# SXCU\nPython API wraper for sxcu.net. Pretty much everything is explained in `doc strings` and soon I will create a tutorial on how to use it.\n\n## Contributing\nPlease refer to [CONTRIBUTING.md](CONTRIBUTING.md) file for more information on how to\ncontribute to this project.\n',
    'author': 'Naveen M K',
    'author_email': 'naveen@syrusdark.website',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
