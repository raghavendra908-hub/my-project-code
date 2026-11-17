"""Shared pytest fixtures for the monitoring demo."""

from __future__ import annotations

import pytest

from app import create_app


@pytest.fixture
def app():
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key-not-for-production",
            "WTF_CSRF_ENABLED": False,
        }
    )
    yield application


@pytest.fixture
def client(app):
    return app.test_client()
