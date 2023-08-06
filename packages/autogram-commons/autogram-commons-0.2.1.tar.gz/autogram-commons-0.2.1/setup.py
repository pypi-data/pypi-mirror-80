# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autogram_commons']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[dotenv]>=1.6.1,<2.0.0', 'ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'autogram-commons',
    'version': '0.2.1',
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
