"""Read-only local host metrics via psutil (no subprocess shell)."""

from __future__ import annotations

from typing import Any

import psutil

PROCESS_LIMIT = 15
PORT_LIMIT = 40
REFRESH_SECONDS = 8


def _bytes_human(num: float) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    value = float(num)
    for unit in units:
        if abs(value) < 1024.0 or unit == units[-1]:
            if unit in ("GB", "TB"):
                return f"{value:.1f} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{num:.0f} B"


def _bytes_gb(num: float) -> str:
    return f"{num / (1024 ** 3):.1f} GB"


def collect_cpu() -> dict[str, Any]:
    try:
        percent = psutil.cpu_percent(interval=0.1)
        return {"percent": round(percent, 1), "error": None}
    except Exception as exc:  # noqa: BLE001 — demo: surface soft errors
        return {"percent": None, "error": str(exc)}


def collect_memory() -> dict[str, Any]:
    try:
        mem = psutil.virtual_memory()
        return {
            "used": mem.used,
            "free": mem.available,
            "total": mem.total,
            "percent": mem.percent,
            "used_h": _bytes_gb(mem.used),
            "free_h": _bytes_gb(mem.available),
            "total_h": _bytes_gb(mem.total),
            "error": None,
        }
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def collect_disk(path: str = "/") -> dict[str, Any]:
    try:
        usage = psutil.disk_usage(path)
        return {
            "path": path,
            "used": usage.used,
            "free": usage.free,
            "total": usage.total,
            "percent": usage.percent,
            "used_h": _bytes_gb(usage.used),
            "free_h": _bytes_gb(usage.free),
            "total_h": _bytes_gb(usage.total),
            "error": None,
        }
    except Exception as exc:  # noqa: BLE001
        return {"path": path, "error": str(exc)}


def collect_load() -> dict[str, Any]:
    try:
        one, five, fifteen = psutil.getloadavg()
        return {
            "one": round(one, 2),
            "five": round(five, 2),
            "fifteen": round(fifteen, 2),
            "error": None,
        }
    except (AttributeError, OSError) as exc:
        return {"error": str(exc)}


def collect_network() -> dict[str, Any]:
    try:
        counters = psutil.net_io_counters(pernic=True) or {}
        # Prefer non-loopback interfaces; fall back to all.
        rows = []
        for name, stats in counters.items():
            if name.startswith("lo"):
                continue
            rows.append(
                {
                    "name": name,
                    "rx": stats.bytes_recv,
                    "tx": stats.bytes_sent,
                    "rx_h": _bytes_human(stats.bytes_recv),
                    "tx_h": _bytes_human(stats.bytes_sent),
                }
            )
        if not rows:
            for name, stats in counters.items():
                rows.append(
                    {
                        "name": name,
                        "rx": stats.bytes_recv,
                        "tx": stats.bytes_sent,
                        "rx_h": _bytes_human(stats.bytes_recv),
                        "tx_h": _bytes_human(stats.bytes_sent),
                    }
                )
        rx_total = sum(r["rx"] for r in rows)
        tx_total = sum(r["tx"] for r in rows)
        return {
            "interfaces": rows[:8],
            "rx_total": rx_total,
            "tx_total": tx_total,
            "rx_total_h": _bytes_human(rx_total),
            "tx_total_h": _bytes_human(tx_total),
            "unit": "cumulative bytes",
            "error": None,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "interfaces": [],
            "rx_total": 0,
            "tx_total": 0,
            "rx_total_h": "0.0 B",
            "tx_total_h": "0.0 B",
            "error": str(exc),
        }


def collect_listening_ports() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    try:
        connections = psutil.net_connections(kind="inet")
    except (psutil.AccessDenied, PermissionError) as exc:
        return {
            "ports": [],
            "tcp": 0,
            "udp": 0,
            "error": f"Limited permissions: {exc}",
            "limit": PORT_LIMIT,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "ports": [],
            "tcp": 0,
            "udp": 0,
            "error": str(exc),
            "limit": PORT_LIMIT,
        }

    seen: set[tuple[str, int, str]] = set()
    tcp = 0
    udp = 0
    for conn in connections:
        if conn.status != psutil.CONN_LISTEN:
            continue
        if not conn.laddr:
            continue
        port = int(conn.laddr.port)
        proto = "tcp" if conn.type.name == "SOCK_STREAM" else "udp"
        key = (proto, port, conn.laddr.ip)
        if key in seen:
            continue
        seen.add(key)
        if proto == "tcp":
            tcp += 1
        else:
            udp += 1
        proc_name = None
        if conn.pid:
            try:
                proc_name = psutil.Process(conn.pid).name()[:64]
            except (psutil.Error, ProcessLookupError):
                proc_name = f"pid:{conn.pid}"
        if len(rows) < PORT_LIMIT:
            rows.append(
                {
                    "port": port,
                    "proto": proto,
                    "address": conn.laddr.ip,
                    "process": proc_name or "—",
                }
            )

    rows.sort(key=lambda r: (r["proto"], r["port"]))
    return {
        "ports": rows,
        "tcp": tcp,
        "udp": udp,
        "error": None,
        "limit": PORT_LIMIT,
    }


def collect_processes(limit: int = PROCESS_LIMIT) -> dict[str, Any]:
    procs: list[dict[str, Any]] = []
    try:
        for proc in psutil.process_iter(
            ["pid", "name", "username", "cpu_percent", "memory_percent"]
        ):
            info = proc.info
            name = (info.get("name") or "?")[:64]
            procs.append(
                {
                    "pid": info.get("pid"),
                    "name": name,
                    "user": (info.get("username") or "—")[:32],
                    "cpu": round(float(info.get("cpu_percent") or 0.0), 1),
                    "mem": round(float(info.get("memory_percent") or 0.0), 1),
                }
            )
    except Exception as exc:  # noqa: BLE001
        return {"processes": [], "error": str(exc), "limit": limit}

    procs.sort(key=lambda p: (p["cpu"], p["mem"]), reverse=True)
    return {"processes": procs[:limit], "error": None, "limit": limit}


def collect_all() -> dict[str, Any]:
    """Gather all dashboard metrics from the local machine only."""
    return {
        "cpu": collect_cpu(),
        "memory": collect_memory(),
        "disk": collect_disk("/"),
        "load": collect_load(),
        "network": collect_network(),
        "ports": collect_listening_ports(),
        "processes": collect_processes(),
        "refresh_seconds": REFRESH_SECONDS,
        "source": "localhost",
    }
