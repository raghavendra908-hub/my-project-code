# UI notes (Phase 0)

## Theme

Custom CSS in `static/css/style.css` — dark / high-contrast ops look (teal accent on deep navy). No Bootstrap or Tailwind; one consistent stack.

## Layout regions

| Region | Role |
|--------|------|
| **Header** | App brand (`Host Monitor`), subtitle, signed-in user + logout |
| **Intro** | Page title + short description |
| **Inventory strip** | Placeholder for server list (later phase) |
| **Metrics grid** | Seven panels: CPU, Memory, Disk, Load, Network, Ports, Processes |
| **Footer** | Localhost-only reminder |
| **Sign in** | `/login` — username/password form with CSRF |

## Panels

Each metric panel has a title, short hint, and a **No data yet** body until `psutil` is wired (Phase 3).
