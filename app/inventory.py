"""In-memory server inventory (demo only — cleared on restart)."""

from __future__ import annotations

import re
import threading
from dataclasses import asdict, dataclass
from itertools import count
from typing import Any

# Control characters and other non-printable noise — never shell-interpolate hosts.
_CTRL = re.compile(r"[\x00-\x1f\x7f]")

_MAX_NAME = 64
_MAX_HOST = 253
_MAX_NOTES = 200

_lock = threading.Lock()
_id_seq = count(1)
_servers: dict[int, "Server"] = {}


@dataclass(frozen=True)
class Server:
    id: int
    name: str
    host: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _clean(value: str, max_len: int) -> str:
    text = _CTRL.sub("", (value or "")).strip()
    return text[:max_len]


def list_servers() -> list[Server]:
    with _lock:
        return list(_servers.values())


def add_server(name: str, host: str, notes: str = "") -> Server:
    """Validate and add a server entry. Raises ValueError on bad input."""
    clean_name = _clean(name, _MAX_NAME)
    clean_host = _clean(host, _MAX_HOST)
    clean_notes = _clean(notes, _MAX_NOTES)

    if not clean_name:
        raise ValueError("Name is required.")
    if not clean_host:
        raise ValueError("Hostname or IP is required.")

    with _lock:
        server_id = next(_id_seq)
        server = Server(
            id=server_id,
            name=clean_name,
            host=clean_host,
            notes=clean_notes,
        )
        _servers[server_id] = server
        return server


def remove_server(server_id: int) -> bool:
    """Remove by id. Returns True if removed."""
    with _lock:
        return _servers.pop(server_id, None) is not None


def clear_servers() -> None:
    """Test helper — empty the inventory."""
    with _lock:
        _servers.clear()


def ensure_demo_localhost() -> Server | None:
    """Seed a localhost inventory row once so the demo is not empty."""
    with _lock:
        if _servers:
            return None
    return add_server("demo-local", "localhost", "default local host")
