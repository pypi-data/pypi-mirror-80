"""Social Auth EPITA pipeline functions

This file contains functions to be used in a python-social-auth pipeline. Two of
these functions (`deny_old_users` and `merge_old_users`) deal with a rare but
inconvenient corner case: username updates. The last function (`update_email`)
force email updates since they are ignored by the default pipeline.

They have only been tested with Django but have been written in a way that
should work with other frameworks.
"""

# pylint: disable=keyword-arg-before-vararg

from social_core.exceptions import AuthForbidden, AuthFailed


def deny_old_users(storage, response, backend, *_args, **_kwargs):
    """This function prevents users with an updated username to sign in with their
    old identity."""

    if backend.name != "epita":
        return {}

    new_login = response.get("new_login", None)
    if not new_login:
        return {}

    social = storage.user.get_social_auth(provider=backend.name, uid=new_login)
    if social:
        raise AuthForbidden(
            backend, f"A new account for this user already exists: {social.user}"
        )

    return {}


def merge_old_users(storage, backend, response, username, user=None, *_args, **_kwargs):
    """Merge old accounts into the new one when a username update is detected.

    For now it is only possible to merge one old account into a new, not
    previously existing, account. This is achieved by updating the old account
    with the new username."""

    if backend.name != "epita":
        return {}

    old_logins = response.get("old_logins", [])
    old_users = set()
    for login in old_logins:
        social = storage.user.get_social_auth(provider=backend.name, uid=login)
        if social:
            old_users.add(social.user)

    if not old_users:
        return {}

    if user:
        old_users_str = ", ".join(old_users)
        raise AuthFailed(backend, f"Cannot merge accounts: {user} and {old_users_str}")

    if len(old_users) > 1:
        old_users_str = ", ".join(old_users)
        raise AuthFailed(backend, f"Too many accounts to merge: {old_users_str}")

    for old_user in old_users:
        old_social_users = storage.user.get_social_auth_for_user(old_user)
        for old_social_user in old_social_users:
            storage.user.disconnect(old_social_user)

    old_user = old_users.pop()

    setattr(old_user, storage.user.username_field(), username)
    storage.user.changed(old_user)

    return {"user": old_user, "is_new": False, "social": None, "new_association": True}


def update_email(storage, backend, details, user=None, *_args, **_kwargs):
    """This function allows email updates to be processed since the default
    social-auth pipeline ignores the email claim for existing accounts."""

    if not user or backend.name != "epita":
        return {}

    email_field = getattr(storage.user.user_model(), "EMAIL_FIELD", "email")
    email = details.get("email")

    if getattr(user, email_field) != email:
        setattr(user, email_field, email)
        storage.user.changed(user)

    return {}
