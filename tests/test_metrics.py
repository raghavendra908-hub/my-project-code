"""Unit tests for local metrics helpers (mocked psutil)."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.auth import ADMIN_USERNAME
from app.metrics import (
    collect_all,
    collect_cpu,
    collect_disk,
    collect_listening_ports,
    collect_load,
    collect_memory,
    collect_network,
    collect_processes,
)

DEMO_PASSWORD = "admin123"


def test_collect_cpu_mocked():
    with patch("app.metrics.psutil.cpu_percent", return_value=12.3):
        data = collect_cpu()
    assert data["percent"] == 12.3
    assert data["error"] is None


def test_collect_memory_mocked():
    mem = SimpleNamespace(used=1000, available=2000, total=4000, percent=25.0)
    with patch("app.metrics.psutil.virtual_memory", return_value=mem):
        data = collect_memory()
    assert data["percent"] == 25.0
    assert data["used"] == 1000
    assert "used_h" in data


def test_collect_disk_mocked():
    usage = SimpleNamespace(used=50, free=50, total=100, percent=50.0)
    with patch("app.metrics.psutil.disk_usage", return_value=usage):
        data = collect_disk("/")
    assert data["path"] == "/"
    assert data["percent"] == 50.0


def test_collect_load_mocked():
    with patch("app.metrics.psutil.getloadavg", return_value=(0.1, 0.2, 0.3)):
        data = collect_load()
    assert data["one"] == 0.1
    assert data["fifteen"] == 0.3


def test_collect_network_skips_loopback_first():
    counters = {
        "lo": SimpleNamespace(bytes_recv=1, bytes_sent=2),
        "eth0": SimpleNamespace(bytes_recv=100, bytes_sent=200),
    }
    with patch("app.metrics.psutil.net_io_counters", return_value=counters):
        data = collect_network()
    names = [row["name"] for row in data["interfaces"]]
    assert "eth0" in names
    assert "lo" not in names


def test_collect_ports_bounded():
    conn = SimpleNamespace(
        status="LISTEN",
        type=SimpleNamespace(name="SOCK_STREAM"),
        laddr=SimpleNamespace(ip="0.0.0.0", port=22),
        pid=None,
    )
    with patch("app.metrics.psutil.CONN_LISTEN", "LISTEN"), patch(
        "app.metrics.psutil.net_connections", return_value=[conn]
    ):
        data = collect_listening_ports()
    assert data["ports"][0]["port"] == 22
    assert data["tcp"] == 1
    assert data["udp"] == 0
    assert data["limit"] >= 1


def test_collect_processes_bounded():
    fake = MagicMock()
    fake.info = {
        "pid": 1,
        "name": "init",
        "username": "root",
        "cpu_percent": 1.0,
        "memory_percent": 0.5,
    }
    with patch("app.metrics.psutil.process_iter", return_value=[fake]):
        data = collect_processes(limit=5)
    assert len(data["processes"]) == 1
    assert data["limit"] == 5


def test_collect_all_shape():
    with patch("app.metrics.collect_cpu", return_value={"percent": 1, "error": None}), patch(
        "app.metrics.collect_memory", return_value={"error": None}
    ), patch("app.metrics.collect_disk", return_value={"error": None}), patch(
        "app.metrics.collect_load", return_value={"error": None}
    ), patch("app.metrics.collect_network", return_value={"interfaces": [], "error": None}    ), patch(
        "app.metrics.collect_listening_ports",
        return_value={"ports": [], "tcp": 0, "udp": 0, "error": None, "limit": 40},
    ), patch(
        "app.metrics.collect_processes",
        return_value={"processes": [], "error": None, "limit": 15},
    ):
        data = collect_all()
    assert data["source"] == "localhost"
    assert "refresh_seconds" in data
    for key in ("cpu", "memory", "disk", "load", "network", "ports", "processes"):
        assert key in data


def test_dashboard_shows_metrics_when_authenticated(client):
    client.post(
        "/login",
        data={"username": ADMIN_USERNAME, "password": DEMO_PASSWORD},
    )
    response = client.get("/")
    assert response.status_code == 200
    assert b"Monitoring dashboard" in response.data
    assert b"panel-cpu" in response.data
    assert b"Auto-refresh" in response.data
    assert b"Manage inventory" in response.data
    assert b"No data yet" not in response.data


def test_dashboard_metrics_require_auth(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
