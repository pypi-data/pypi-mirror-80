social-auth-backend-epita
=========================

Pluggable authentication backend for `python-social-auth` that allows
authentication with the CRI OpenID Connect provider.

## Installation instructions

```sh
$ pip install social-auth-backend-epita --index-url https://gitlab.cri.epita.fr/api/v4/projects/515/packages/pypi/simple
```

## Configuration instructions

### Django

**You should take a look at [our example project] to see how to properly use
this package.**

[our example project]:
https://gitlab.cri.epita.fr/cri/documentation/django-social-auth-epita-example


1. Add `social_auth_backend_epita.backend.EpitaOpenIdConnect` to
   the `AUTHENTICATION_BACKENDS` of your Django `settings.py` file:

```python
AUTHENTICATION_BACKENDS = (
    "social_auth_backend_epita.backend.EpitaOpenIdConnect",
    "django.contrib.auth.backends.ModelBackend",
)
```

2. Add your OpenID client credentials to your Django `settings.py` file:

```python
SOCIAL_AUTH_EPITA_KEY = "..."
SOCIAL_AUTH_EPITA_SECRET = "..."
```

3. Fill `SOCIAL_AUTH_EPITA_SCOPE` with the relevant scope names in your Django
`settings.py` file:

```python
SOCIAL_AUTH_EPITA_SCOPE = [
    "email",
    "epita",
]
```

### Other frameworks

This backend only uses framework-agnostic functions and should work with any
framework supported by python-social-auth. Be advised that it has only been
tested with Django.

## Pipeline functions

You may add the following functions to your social auth pipeline:

### `social_auth_backend_epita.pipeline.deny_old_users`

This function prevents users with an updated username to sign in with their old
identity.

### `social_auth_backend_epita.pipeline.merge_old_users`

Merge old accounts into the new one when a username update is detected.

For now it is only possible to merge one old account into a new, not previously
existing, account. This is achieved by updating the old account with the new
username.

### `social_auth_backend_epita.pipeline.update_email`

This function allows email updates to be processed since the default
social-auth pipeline ignores the email claim for existing accounts.
