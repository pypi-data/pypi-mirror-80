# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['roamnerd_private_cli']
install_requires = \
['argh>=0.26.2,<0.27.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'spacy>=2.3.2,<3.0.0']

entry_points = \
{'console_scripts': ['RoamnerdInstance = RoamnerdInstance',
                     'roamNERdHelper = roamnerdHelper',
                     'roamnerdMain = roamnerdMain',
                     'roamnerd_private_cli = roamnerd_private_cli:main']}

setup_kwargs = {
    'name': 'roamnerd-private-cli',
    'version': '0.1.1',
    'description': 'A private CLI for roamNERd developers / power users. Runs all NER locally using spacy',
    'long_description': None,
    'author': 'hmprt',
    'author_email': 'hmprt@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
