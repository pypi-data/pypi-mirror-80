# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['task']

package_data = \
{'': ['*']}

install_requires = \
['click-default-group>=1.2.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'task',
    'version': '0.1.1',
    'description': 'Task cli tool',
    'long_description': None,
    'author': 'matteyeux',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
