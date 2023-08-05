# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_datastructures']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-datastructures',
    'version': '0.1.0',
    'description': 'Python datastructures package',
    'long_description': None,
    'author': 'Tomasz Turek',
    'author_email': 'ttomaszito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
