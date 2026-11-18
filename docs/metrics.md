# Metrics (Phase 3)

All metrics are read-only via `psutil` on the **local** host (`source: localhost`).

| Panel | Source | Units / notes |
|-------|--------|----------------|
| CPU | `cpu_percent` | Overall % |
| Memory | `virtual_memory` | Used / available / % |
| Disk | `disk_usage("/")` | Root filesystem used / free / % |
| Load | `getloadavg` | 1 / 5 / 15 minute |
| Network | `net_io_counters(pernic=True)` | Cumulative RX/TX bytes (humanized); non-loopback preferred |
| Listening ports | `net_connections` (LISTEN) | Bound to 40 rows; process name if permitted |
| Processes | `process_iter` | Top 15 by CPU then memory; names truncated; **no kill** |

## Refresh

Dashboard auto-refreshes every **8 seconds** (`REFRESH_SECONDS` in `app/metrics.py`) via HTML meta refresh on `/` only (authenticated session).

## Permissions

Some hosts restrict `net_connections` or process details; the UI shows a soft error and continues.
