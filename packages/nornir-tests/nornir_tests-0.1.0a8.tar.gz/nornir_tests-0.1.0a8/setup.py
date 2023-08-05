# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_tests',
 'nornir_tests.plugins',
 'nornir_tests.plugins.functions',
 'nornir_tests.plugins.tasks',
 'nornir_tests.plugins.tests']

package_data = \
{'': ['*']}

install_requires = \
['assertpy>=1.1,<2.0',
 'jsonpath-ng>=1.5.2,<2.0.0',
 'lxml>=4.5.2,<5.0.0',
 'nornir',
 'wrapt>=1.12.1,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'nornir-tests',
    'version': '0.1.0a8',
    'description': 'Testing extension for Nornir',
    'long_description': None,
    'author': 'Patrick Avery',
    'author_email': 'patrickdaj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/patrickdaj/nornir_tests',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
