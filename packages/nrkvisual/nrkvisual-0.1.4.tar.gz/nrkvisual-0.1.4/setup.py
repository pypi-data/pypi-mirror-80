# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nrkvisual', 'nrkvisual.tkhelper', 'nrkvisual.visual']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0.4,<4.0.0',
 'matplotlib>=3.3.2,<4.0.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.2,<2.0.0',
 'xlrd>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'nrkvisual',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@mjaquier.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
