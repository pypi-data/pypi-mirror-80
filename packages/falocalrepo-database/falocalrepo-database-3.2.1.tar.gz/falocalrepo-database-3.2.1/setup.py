# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['falocalrepo_database']

package_data = \
{'': ['*']}

install_requires = \
['faapi==2.8.3', 'filetype==1.0.7']

setup_kwargs = {
    'name': 'falocalrepo-database',
    'version': '3.2.1',
    'description': 'Database functionality for falocalrepo.',
    'long_description': None,
    'author': 'Matteo Campinoti',
    'author_email': 'matteo.campinoti94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/MatteoCampinoti94/falocalrepo-database',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
