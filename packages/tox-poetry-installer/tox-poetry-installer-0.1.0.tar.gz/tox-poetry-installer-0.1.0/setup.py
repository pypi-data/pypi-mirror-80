# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tox_poetry_installer']
install_requires = \
['poetry>=1.0.0,<2.0.0', 'tox>=2.3.0,<4.0.0']

entry_points = \
{'tox': ['poetry_installer = tox_poetry_installer']}

setup_kwargs = {
    'name': 'tox-poetry-installer',
    'version': '0.1.0',
    'description': 'Tox plugin to install Tox environment dependencies using the Poetry backend and lockfile',
    'long_description': None,
    'author': 'Ethan Paul',
    'author_email': 'e@enp.one',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/enpaul/tox-poetry-installer/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
