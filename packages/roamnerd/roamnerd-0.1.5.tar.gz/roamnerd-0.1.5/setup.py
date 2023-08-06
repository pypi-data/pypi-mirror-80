# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['roamnerd']
install_requires = \
['argh>=0.26.2,<0.27.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['roamnerd = roamnerd:main']}

setup_kwargs = {
    'name': 'roamnerd',
    'version': '0.1.5',
    'description': 'A command-line tool for accessing the roamNERd API to annotate .txt files',
    'long_description': None,
    'author': 'hmprt',
    'author_email': 'hmprt@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
