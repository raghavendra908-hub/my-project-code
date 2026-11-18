# TODO: Demo Linux Server Monitoring (Local)

Incremental checklist for AI-assisted development. Each step is small, ships with **security** and **documentation**, and keeps the demo runnable locally only.

Reference: [requirements.md](./requirements.md)

---

## Phase 0 — Project initialization & Basic UI

- [x] **0.1** Create project layout (`app/`, `templates/`, `static/`, `tests/`, `docs/`) and a root `README.md` describing the demo purpose and local-only scope.
  - Security: note that the app binds to localhost and must not be exposed publicly.
  - Docs: one-paragraph overview + intended audience (internal demo).

- [x] **0.2** Add `requirements.txt` with pinned deps (`flask`, `psutil`, `werkzeug`) and document install steps in `README.md` (venv + `pip install -r requirements.txt`).
  - Security: pin versions; do not commit secrets or `.env` with real credentials.
  - Docs: copy-paste install commands only (minimal).

- [x] **0.3** Scaffold a minimal Flask app (`app.py` or `app/__init__.py`) that serves a single home/landing page on `127.0.0.1`.
  - Security: bind to `127.0.0.1` by default; disable debug in any shared notes.
  - Docs: “how to start” (`python app.py`) and default URL.

- [x] **0.4** Add Basic UI shell: Jinja base template + CSS (one consistent stack), dark/high-contrast ops look, header with app name.
  - Security: set a strong `SECRET_KEY` via env or generated local default; never hardcode production secrets.
  - Docs: short note in `docs/ui.md` on theme choice and layout regions (header / content).

- [x] **0.5** Add empty placeholder panels on the dashboard page (CPU, Memory, Disk, Load, Network, Ports, Processes) with “no data yet” labels—no metrics wired yet.
  - Security: page may be public temporarily; document that auth lands in the next phase.
  - Docs: update README with a screenshot placeholder or panel list matching the PRD.

---

## Phase 1 — Sign-in & unit tests

- [x] **1.1** Add single built-in user `admin` with password stored only as a hash (Werkzeug/`pbkdf2`); default demo password `admin123` documented for local demo.
  - Security: never store or log plaintext passwords; hash at seed time.
  - Docs: document default credentials and that they are demo-only in `README.md`.

- [x] **1.2** Implement login route + form (username + password); reject invalid credentials with a clear flash/message; redirect to dashboard on success.
  - Security: POST-only login; CSRF protection (Flask-WTF or equivalent) if feasible in demo scope; constant-time hash check via Werkzeug.
  - Docs: document login URL and failure behavior in `docs/auth.md`.

- [x] **1.3** Protect all monitoring/inventory routes behind login; unauthenticated users redirect to login; add logout that clears the session.
  - Security: session cookie `HttpOnly`; `SameSite=Lax`; secure flag guidance for HTTPS if ever used.
  - Docs: update acceptance note—unauthenticated users cannot see metrics.

- [x] **1.4** Write unit tests for auth: valid login, invalid login, logout, protected-route redirect, password not stored in plaintext.
  - Security: tests assert hash-only storage and 401/redirect behavior.
  - Docs: document how to run tests (`pytest`) in `README.md`.

- [x] **1.5** Add `pytest` (and Flask test client helpers) to dev dependencies; ensure tests pass locally.
  - Security: no real secrets in test fixtures beyond the documented demo hash/password.
  - Docs: add a “Testing” subsection with one command.

---

## Phase 2 — Local server inventory (in-memory)

- [x] **2.1** In-memory server list model (name/label, hostname/IP, optional notes/tags); seed nothing remote—demo expects `localhost` / `127.0.0.1`.
  - Security: sanitize/trim inputs; enforce max lengths; no shell interpolation of hostname fields.
  - Docs: document inventory fields and “restart clears list” in `docs/inventory.md`.

- [x] **2.2** Add-server form (auth required); validate required fields; show clear UI note that live metrics always come from the local machine.
  - Security: reject unexpected fields; escape all output in templates (Jinja auto-escape on).
  - Docs: note localhost-only metrics rule on the form help text and in docs.

- [x] **2.3** List servers and remove-from-list action (auth required, POST for delete); confirm UI is inventory-only (no SSH/agents).
  - Security: POST + session required for delete; no mass-assignment of internal IDs from client beyond list index/id you control.
  - Docs: update `docs/inventory.md` with add/list/remove flows.

- [x] **2.4** Unit tests for add/list/remove and auth gating on inventory routes.
  - Security: tests confirm unauthenticated access is blocked.
  - Docs: mention inventory tests under Testing in README.

---

## Phase 3 — Local metrics (read-only)

- [x] **3.1** Add a small metrics helper using `psutil` for CPU % (one call pattern suitable for demo).
  - Security: read-only APIs only; no subprocess shell for metrics.
  - Docs: `docs/metrics.md` — CPU source and units.

- [x] **3.2** Add memory (used/free/+%) and disk (root/primary used/free/%) to the helper and dashboard panels.
  - Security: handle permission errors gracefully; never expose arbitrary path reads beyond intended filesystem stats.
  - Docs: document which mount/path is shown.

- [x] **3.3** Add load average (1/5/15) and network RX/TX (primary interfaces) panels.
  - Security: do not dump full interface config secrets; show names/counters only.
  - Docs: document refresh semantics and units (bytes vs rates).

- [x] **3.4** Add listening ports table (port, proto, process if available) and bounded process list (top 10–20 by CPU/memory).
  - Security: read-only; no kill/signal actions; bound list size to avoid huge responses.
  - Docs: document bounds and “process if available” caveat.

- [x] **3.5** Wire dashboard to live local metrics; keep a visible note that telemetry is localhost regardless of inventory hostname.
  - Security: metrics endpoints/pages require auth.
  - Docs: update acceptance checklist progress in README or `docs/metrics.md`.

- [x] **3.6** Unit/integration tests for metrics helpers (mock `psutil` where needed) and auth on dashboard.
  - Security: tests ensure no unauthenticated metrics JSON/HTML.
  - Docs: how to run metrics-related tests.

---

## Phase 4 — Auto-refresh & UI polish

- [x] **4.1** Add dashboard auto-refresh (meta refresh or minimal JS poll), default interval 5–10 seconds; make interval obvious in UI.
  - Security: refresh only hits same-origin authenticated routes; no eval of remote scripts.
  - Docs: document default interval and how to change it (one config constant).

- [x] **4.2** Polish layout: header (app name + user + logout), inventory strip, metric panels with clear hierarchy; responsive enough for laptop.
  - Security: ensure logout control is always visible when authenticated.
  - Docs: update `docs/ui.md` with final layout map.

- [x] **4.3** Pass a quick manual demo script: login → add `localhost` → watch panels refresh → logout.
  - Security: confirm post-logout dashboard is inaccessible.
  - Docs: add “Demo walkthrough” (5 steps) to README matching PRD §6.

---

## Phase 5 — CI/CD (GitHub Actions) & final docs

- [x] **5.1** Add `.github/workflows/ci.yml`: on push/PR, set up Python, install deps, run `pytest`, fail on test failures.
  - Security: no secrets in workflow logs; use least-privilege `permissions:` (e.g. `contents: read`).
  - Docs: document CI status badge optional; explain what CI runs in `docs/ci.md`.

- [x] **5.2** Add lint/format check in CI if lightweight (e.g. `ruff` or `flake8`)—keep config minimal.
  - Security: pin action versions (`@v4` SHA or tagged releases).
  - Docs: note local lint command in README.

- [x] **5.3** Final README pass: install, run, login, test, CI—minimal instructions only; link to `docs/requirements.md` and this TODO.
  - Security: restate localhost binding, hashed password, read-only UI, demo credentials warning.
  - Docs: mark acceptance criteria in PRD or a short `docs/acceptance.md` checklist as done when verified.

- [x] **5.4** Smoke-verify acceptance criteria from PRD §7 on the local machine; check off items when confirmed.
  - Security: re-verify unauthenticated access blocked and no write/kill controls exist.
  - Docs: record “verified locally” date/note in `docs/acceptance.md`.

---

## Suggested order (summary)

1. Init + Basic UI (Phase 0)  
2. Sign-in + unit tests (Phase 1)  
3. In-memory server inventory (Phase 2)  
4. Local read-only metrics (Phase 3)  
5. Auto-refresh + polish (Phase 4)  
6. GitHub Actions CI + final docs (Phase 5)  

**Out of scope (do not implement):** remote SSH/agents, Windows hosts, alerts/history, multi-role auth, host mutations, cloud/Docker deploy.
