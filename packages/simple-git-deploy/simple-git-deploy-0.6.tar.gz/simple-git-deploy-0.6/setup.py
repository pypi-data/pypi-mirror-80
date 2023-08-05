# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['simple_git_deploy']
install_requires = \
['laika-deploy>=0.6,<0.7']

entry_points = \
{'console_scripts': ['laika = laika.cli:main',
                     'simple-git-deploy = laika.cli:main']}

setup_kwargs = {
    'name': 'simple-git-deploy',
    'version': '0.6',
    'description': 'A command-line utility for easy and reliable management of manual deployments from Git repositories',
    'long_description': '# Laika 🐶\n\n`simple-git-deploy` has been renamed. Please check the new links:\n\n* GitHub, https://github.com/edudobay/laika\n* PyPI, https://pypi.org/project/laika-deploy/\n',
    'author': 'Eduardo Dobay',
    'author_email': 'edudobay@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/edudobay/laika',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
