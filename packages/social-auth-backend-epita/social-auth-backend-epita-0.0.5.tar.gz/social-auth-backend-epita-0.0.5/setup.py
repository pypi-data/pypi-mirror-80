# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epita_connect']

package_data = \
{'': ['*']}

install_requires = \
['social-auth-core[openidconnect]>=3.3.3,<4.0.0']

setup_kwargs = {
    'name': 'social-auth-backend-epita',
    'version': '0.0.5',
    'description': 'EPITA backend for python-social-auth',
    'long_description': None,
    'author': 'Marin Hannache',
    'author_email': 'mareo@cri.epita.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.cri.epita.fr/cri/packages/social-auth-backend-epita',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
