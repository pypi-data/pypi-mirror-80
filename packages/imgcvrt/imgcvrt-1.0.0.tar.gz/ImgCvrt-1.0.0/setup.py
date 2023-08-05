# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['imgcvrt']
setup_kwargs = {
    'name': 'imgcvrt',
    'version': '1.0.0',
    'description': 'Convert("filename").toIco("filename")',
    'long_description': None,
    'author': 'TimurALTron',
    'author_email': 'slaveallaha7777@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
