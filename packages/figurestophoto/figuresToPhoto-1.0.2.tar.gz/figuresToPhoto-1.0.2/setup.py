# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['figurestophoto']
setup_kwargs = {
    'name': 'figurestophoto',
    'version': '1.0.2',
    'description': 'figures("test.png").squareToJpg(20,20,100,100,"black","blackTest")',
    'long_description': None,
    'author': 'RealGames70',
    'author_email': '69468716+RealGames70@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
