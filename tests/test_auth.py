"""Unit tests for sign-in, logout, and route protection."""

from __future__ import annotations

from pathlib import Path

from werkzeug.security import check_password_hash

from app.auth import ADMIN_PASSWORD_HASH, ADMIN_USERNAME, verify_credentials

DEMO_PASSWORD = "admin123"


def test_password_stored_as_hash_only():
    assert ADMIN_PASSWORD_HASH.startswith(("scrypt:", "pbkdf2:"))
    assert DEMO_PASSWORD not in ADMIN_PASSWORD_HASH
    auth_source = Path("app/auth.py").read_text(encoding="utf-8")
    assert DEMO_PASSWORD not in auth_source
    assert check_password_hash(ADMIN_PASSWORD_HASH, DEMO_PASSWORD)


def test_verify_credentials_accepts_admin():
    assert verify_credentials(ADMIN_USERNAME, DEMO_PASSWORD) is True


def test_verify_credentials_rejects_invalid():
    assert verify_credentials(ADMIN_USERNAME, "wrong-password") is False
    assert verify_credentials("other", DEMO_PASSWORD) is False


def test_dashboard_requires_login(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign in" in response.data


def test_valid_login_redirects_to_dashboard(client):
    response = client.post(
        "/login",
        data={"username": ADMIN_USERNAME, "password": DEMO_PASSWORD},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    dashboard = client.get("/")
    assert dashboard.status_code == 200
    assert b"Monitoring dashboard" in dashboard.data
    assert b"admin" in dashboard.data


def test_invalid_login_shows_error(client):
    response = client.post(
        "/login",
        data={"username": ADMIN_USERNAME, "password": "nope"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Invalid username or password." in response.data
    assert b"Monitoring dashboard" not in response.data


def test_logout_clears_session(client):
    client.post(
        "/login",
        data={"username": ADMIN_USERNAME, "password": DEMO_PASSWORD},
    )
    response = client.post("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    blocked = client.get("/", follow_redirects=False)
    assert blocked.status_code == 302
    assert "/login" in blocked.headers["Location"]


def test_session_cookie_flags(app):
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"


def test_login_rejects_missing_csrf():
    """CSRF must be enforced when enabled (not disabled as in most unit tests)."""
    from app import create_app

    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "csrf-test-secret",
            "WTF_CSRF_ENABLED": True,
        }
    )
    csrf_client = application.test_client()
    response = csrf_client.post(
        "/login",
        data={"username": ADMIN_USERNAME, "password": DEMO_PASSWORD},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Sign in" in response.data
    assert b"Monitoring dashboard" not in response.data
    assert b"form expired" in response.data.lower() or b"csrf" in response.data.lower() or b"Sign in" in response.data
