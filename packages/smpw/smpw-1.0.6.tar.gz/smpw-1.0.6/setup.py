# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['smpw']
setup_kwargs = {
    'name': 'smpw',
    'version': '1.0.6',
    'description': 'modile hack python is windows 10',
    'long_description': None,
    'author': 'John Smith',
    'author_email': 'azarovnick@bk.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
