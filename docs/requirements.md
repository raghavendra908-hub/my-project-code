# PRD: Demo Linux Server Monitoring (Local)

## 1. Overview

Local demo web app to view **read-only** real-time host metrics for the **machine where the app runs** (Linux). Removes the need to SSH in just to check CPU, memory, disk, network, ports, load, and processes.

**Audience:** Internal L1 / L2 / L3 and app/infra teams (demo only).  
**Deploy:** Run locally on the same Cursor/host machine.  
**Stack:** Python, Flask, server-rendered UI (attractive, ops-friendly).

---

## 2. Goals & non-goals

### Goals
- Sign in as a single admin user with a hashed password.
- Register the local Linux host in a simple server list.
- Show live metrics on one dashboard with auto-refresh.
- Keep implementation and run steps minimal for a demo.

### Non-goals (out of scope)
- Remote SSH / agent-based monitoring of other machines
- Windows (or non-Linux) hosts
- Alerts, notifications, thresholds
- Historical metrics, charts over time, or long-term storage
- Multi-user roles (L1/L2/L3 distinctions)
- Write/change actions on the host (UI is read-only)

---

## 3. Users & access

| Item | Requirement |
|------|-------------|
| Users | Single built-in account: `admin` |
| Default password | `admin123` (documented for demo; changeable later if needed) |
| Storage of password | Store only a **hash** (e.g. Werkzeug/`pbkdf2` or similar), never plain text |
| Session | Login required for all monitoring pages; logout available |
| Authorization | All authenticated views are **read-only** |

---

## 4. Features

### 4.1 Sign in
- Login page with username + password.
- Default credentials: **admin** / **admin123**.
- Reject invalid credentials with a clear message.
- After login, land on the monitoring dashboard.

### 4.2 Add server (local only)
- Form to add a server entry for demo inventory.
- Required fields: **name/label**, **hostname or IP** (use `localhost` / `127.0.0.1` for this demo).
- Optional: short notes/tags.
- **Runtime rule:** Metrics are collected **only from the local machine**. Adding other hosts is allowed for UI demo of inventory, but live metrics still reflect localhost (show a clear note on the UI).
- List added servers; allow remove from the in-memory list.
- No SSH keys, agents, or remote collection in v1.

### 4.3 Monitoring dashboard (single page)
One dashboard (no separate detail page in this demo) showing:

| Metric | What to show |
|--------|----------------|
| CPU | Overall CPU usage % |
| Memory | Used and free (absolute + % if easy) |
| Disk | Usage for root (or primary) filesystem: used/free/% |
| Load average | 1 / 5 / 15 minute load |
| Network | RX/TX rates or cumulative bytes for primary interface(s) |
| Listening ports | Local listening TCP/UDP ports (port, proto, process if available) |
| Process list | Top processes by CPU/memory (bounded list, e.g. top 10–20) |

**Auto-refresh:** Dashboard refreshes automatically (suggested default **5–10 seconds**), without full manual reload friction (meta refresh or lightweight JS poll is fine).

**Read-only:** No kill process, no config edit, no shell.

### 4.4 UI look (must-have)
- Clean, modern **ops/monitoring** look: dark or high-contrast theme preferred for demo polish.
- Clear hierarchy: header (app name + user + logout), server inventory strip, metric panels.
- Readable numbers and tables; responsive enough for laptop browser.
- Flask templates + CSS (Bootstrap, Tailwind, or custom CSS—pick one and stay consistent).
- Avoid clutter; one job per panel.

---

## 5. Technical requirements

| Area | Choice |
|------|--------|
| Language | Python 3 |
| Framework | Flask |
| Frontend | Jinja2 templates + CSS (+ minimal JS for refresh if needed) |
| Metrics source | Local OS APIs (e.g. `psutil`) on the host running Flask |
| Auth | Session cookie + hashed password for `admin` |
| Persistence | **In-memory only** (server list + session). Restart clears inventory; default admin remains code/config seeded |
| Config | Defaults in code or a small local config; no external DB |

---

## 6. Minimal run (demo)

1. Create/activate a Python venv and install dependencies (`flask`, `psutil`, etc.).
2. Start the app (e.g. `python app.py` or `flask run`) on localhost.
3. Open the browser to the local URL (e.g. `http://127.0.0.1:5000`).
4. Sign in with `admin` / `admin123`.
5. Add local server (`localhost`), view auto-refreshing dashboard.

No cloud deploy, no Docker requirement, no remote agents for this demo.

---

## 7. Acceptance criteria

Verified in [acceptance.md](./acceptance.md) (2026-11-17):

- [x] Unauthenticated users cannot see metrics.
- [x] Login works with `admin` / `admin123`; password is stored hashed.
- [x] User can add/list/remove server entries in memory.
- [x] Dashboard shows CPU, memory, disk, load average, network RX/TX, listening ports, and a bounded process list from the **local** machine.
- [x] Dashboard auto-refreshes.
- [x] UI is read-only and visually polished for a demo.
- [x] App runs locally with a short install/start path.

---

## 8. Assumptions

- Demo host is Linux (or Linux-like metrics via `psutil`).
- Single concurrent demo user is enough.
- In-memory inventory loss on restart is acceptable.
- “Add server” is inventory UX; live telemetry is localhost-only for this demo.
