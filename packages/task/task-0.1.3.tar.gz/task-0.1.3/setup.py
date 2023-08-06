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

entry_points = \
{'console_scripts': ['pytask = task.main:main', 'task = task.main:main']}

setup_kwargs = {
    'name': 'task',
    'version': '0.1.3',
    'description': 'Task cli tool',
    'long_description': '# task\n\n[![Build Status](http://drone.matteyeux.com:8080/api/badges/matteyeux/task/status.svg)](http://drone.matteyeux.com:8080/matteyeux/task)\n\nTaskwarrior-like CLI tool\n\n```\nUsage: task [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -v, --version  print version\n  --help         Show this message and exit.\n\nCommands:\n  add   Add task\n  done  Finished task.\n  ls    List tasks.\n  rm    Remove a task.\n```\n\n### Installation\n\nMake sure to have [poetry](https://pypi.org/project/poetry)\n\n#### Github repository\n```bash\n$ git clone https://github.com/matteyeux/task\n$ cd task\n$ poetry install\n```\n\n#### PyPI\n- Installation : `pip3 install task`\n- Update : `pip3 install --upgrade task`\n\n### Setup\n\nMake sure to have `~/.local/bin` in your `$PATH` (`export PATH=$PATH:~/.local/bin`)\n\nThe first time you run `task add` command it will setup the SQLite3 database.\n\n\n### Examples\n\n\n\n### Credits\nPowered by [etnawrapper](https://github.com/tbobm/etnawrapper)\n',
    'author': 'matteyeux',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matteyeux/task',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
