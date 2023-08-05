# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newp', 'newp.projects']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0', 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['newp = newp.cli:main']}

setup_kwargs = {
    'name': 'newp',
    'version': '0.0.6',
    'description': 'Spins up new projects',
    'long_description': None,
    'author': 'Tim Simpson',
    'author_email': 'timsimpson4@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TimSimpson/newp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
