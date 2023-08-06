# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dotenv_flow']
install_requires = \
['black>=20.8b1,<21.0', 'python-dotenv>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'dotenv-flow',
    'version': '0.2.0',
    'description': 'Like the dotenv-flow NodeJS library, for Python',
    'long_description': None,
    'author': 'Carlos Gonzalez',
    'author_email': 'gonsa.carlos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
