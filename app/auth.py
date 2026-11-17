"""Built-in demo admin auth (hashed password only)."""

from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar

from flask import redirect, session, url_for
from werkzeug.security import check_password_hash

F = TypeVar("F", bound=Callable[..., object])

# Single demo account. Password plaintext is documented in README / docs/auth.md only —
# never store or log the plaintext password here.
ADMIN_USERNAME = "admin"

# Precomputed Werkzeug hash for the documented demo password.
# Generated with werkzeug.security.generate_password_hash(..., method="scrypt").
ADMIN_PASSWORD_HASH = (
    "scrypt:32768:8:1$uJwCJ3FwZRiD14pQ$"
    "d2e17ce5f10f144bddd370994f2b060dd9c60eb00e8de041340003e82b9303d19a"
    "483c677d8ca58cb96dbe8ee337d7019268b452eaae01f95a8ab4ea3cd5d9e5"
)

SESSION_USER_KEY = "user"


def verify_credentials(username: str, password: str) -> bool:
    """Return True if username/password match the seeded admin hash."""
    if username != ADMIN_USERNAME:
        return False
    return check_password_hash(ADMIN_PASSWORD_HASH, password)


def login_user(username: str) -> None:
    session.clear()
    session[SESSION_USER_KEY] = username
    session.permanent = False


def logout_user() -> None:
    session.clear()


def current_user() -> str | None:
    return session.get(SESSION_USER_KEY)


def is_authenticated() -> bool:
    return current_user() is not None


def login_required(view: F) -> F:
    """Redirect anonymous users to the login page."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped  # type: ignore[return-value]
