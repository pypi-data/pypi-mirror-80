# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paraminjector']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'paraminjector',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Joscha Götzer',
    'author_email': 'joscha.goetzer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
