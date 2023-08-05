# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mineop']
setup_kwargs = {
    'name': 'mineop',
    'version': '1.0.0',
    'description': 'Welcome()',
    'long_description': None,
    'author': 'ALEX9595YT',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
