# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['social_auth_backend_epita']

package_data = \
{'': ['*']}

install_requires = \
['social-auth-core[openidconnect]>=3.3.3,<4.0.0']

setup_kwargs = {
    'name': 'social-auth-backend-epita',
    'version': '1.0.1',
    'description': 'EPITA backend for python-social-auth',
    'long_description': 'social-auth-backend-epita\n=========================\n\nPluggable authentication backend for `python-social-auth` that allows\nauthentication with the CRI OpenID Connect provider.\n\n## Installation instructions\n\n```sh\n$ pip install social-auth-backend-epita --index-url https://gitlab.cri.epita.fr/api/v4/projects/515/packages/pypi/simple\n```\n\n## Configuration instructions\n\n### Django\n\n**You should take a look at [our example project] to see how to properly use\nthis package.**\n\n[our example project]:\nhttps://gitlab.cri.epita.fr/cri/documentation/django-social-auth-epita-example\n\n\n1. Add `social_auth_backend_epita.backend.EpitaOpenIdConnect` to\n   the `AUTHENTICATION_BACKENDS` of your Django `settings.py` file:\n\n```python\nAUTHENTICATION_BACKENDS = (\n    "social_auth_backend_epita.backend.EpitaOpenIdConnect",\n    "django.contrib.auth.backends.ModelBackend",\n)\n```\n\n2. Add your OpenID client credentials to your Django `settings.py` file:\n\n```python\nSOCIAL_AUTH_EPITA_KEY = "..."\nSOCIAL_AUTH_EPITA_SECRET = "..."\n```\n\n3. Fill `SOCIAL_AUTH_EPITA_SCOPE` with the relevant scope names in your Django\n`settings.py` file:\n\n```python\nSOCIAL_AUTH_EPITA_SCOPE = [\n    "email",\n    "epita",\n]\n```\n\n### Other frameworks\n\nThis backend only uses framework-agnostic functions and should work with any\nframework supported by python-social-auth. Be advised that it has only been\ntested with Django.\n\n## Pipeline functions\n\nYou may add the following functions to your social auth pipeline:\n\n### `social_auth_backend_epita.pipeline.deny_old_users`\n\nThis function prevents users with an updated username to sign in with their old\nidentity.\n\n### `social_auth_backend_epita.pipeline.merge_old_users`\n\nMerge old accounts into the new one when a username update is detected.\n\nFor now it is only possible to merge one old account into a new, not previously\nexisting, account. This is achieved by updating the old account with the new\nusername.\n\n### `social_auth_backend_epita.pipeline.update_email`\n\nThis function allows email updates to be processed since the default\nsocial-auth pipeline ignores the email claim for existing accounts.\n',
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
