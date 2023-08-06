# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['new_proj']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'new-proj',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Siddharth Gupta',
    'author_email': 'sid@granular.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
