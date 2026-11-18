"""Unit tests for in-memory server inventory."""

from __future__ import annotations

import pytest

from app.auth import ADMIN_USERNAME
from app.inventory import add_server, clear_servers, list_servers, remove_server

DEMO_PASSWORD = "admin123"


@pytest.fixture(autouse=True)
def _empty_inventory():
    clear_servers()
    yield
    clear_servers()


def _login(client):
    return client.post(
        "/login",
        data={"username": ADMIN_USERNAME, "password": DEMO_PASSWORD},
    )


def test_add_list_remove_model():
    server = add_server("demo", "localhost", "tag")
    assert server.name == "demo"
    assert server.host == "localhost"
    assert list_servers()[0].id == server.id
    assert remove_server(server.id) is True
    assert list_servers() == []


def test_add_rejects_empty_name():
    with pytest.raises(ValueError):
        add_server("  ", "localhost")


def test_inventory_requires_login(client):
    response = client.post(
        "/servers",
        data={"name": "x", "host": "localhost"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

    blocked = client.post(
        "/servers/remove",
        data={"server_id": "1"},
        follow_redirects=False,
    )
    assert blocked.status_code == 302
    assert "/login" in blocked.headers["Location"]

    page = client.get("/servers", follow_redirects=False)
    assert page.status_code == 302
    assert "/login" in page.headers["Location"]


def test_add_and_remove_via_http(client):
    _login(client)
    added = client.post(
        "/servers",
        data={"name": "local", "host": "127.0.0.1", "notes": "demo"},
        follow_redirects=True,
    )
    assert added.status_code == 200
    assert b"local" in added.data
    assert b"127.0.0.1" in added.data
    assert list_servers()

    target = list_servers()[0]
    removed = client.post(
        "/servers/remove",
        data={"server_id": str(target.id)},
        follow_redirects=False,
    )
    assert removed.status_code == 302
    assert list_servers() == []
