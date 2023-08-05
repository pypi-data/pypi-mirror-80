# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aminoraid']
install_requires = \
['Amino.py==1.1.7']

setup_kwargs = {
    'name': 'aminoraid',
    'version': '1.1.2',
    'description': '',
    'long_description': None,
    'author': 'Some Community',
    'author_email': 'olegskvorcovn1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
