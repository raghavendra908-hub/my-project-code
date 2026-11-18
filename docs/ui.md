# UI notes

## Theme

Custom CSS in `static/css/style.css` — dark / high-contrast ops look (teal accent on deep navy).

## Layout map

| Region | Role |
|--------|------|
| **Header** | Brand, signed-in user, refresh interval pill, logout |
| **Intro** | Title + localhost telemetry banner |
| **Inventory strip** | List / add / remove servers (in-memory) |
| **Metrics grid** | CPU, Memory, Disk, Load, Network, Ports, Processes |
| **Sign in** | `/login` — username/password + CSRF |
| **Footer** | Localhost-only reminder |

## Refresh

Meta refresh every 8 seconds on the dashboard only (`REFRESH_SECONDS`).
