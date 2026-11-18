# Host Monitor (Local Demo)

Read-only web UI for live Linux host metrics (CPU, memory, disk, load, network, ports, processes) on the **same machine** where the app runs. Internal L1/L2/L3 demo — not for public or multi-host production use.

**Security:** Binds to `127.0.0.1` only. Passwords hashed. CSRF on forms. Metrics are read-only (no kill/shell). Do not commit secrets or a real `.env`. See [docs/security.md](docs/security.md).

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For tests / lint:

```bash
pip install -r requirements-dev.txt
```

## Run

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) → redirected to `/login`.

If port 5000 is busy:

```bash
PORT=5010 python app.py
```

Optional: `export SECRET_KEY=...` (otherwise a stable local-demo default is used).

## Sign in (demo)

| Username | Password |
|----------|----------|
| `admin` | `admin123` |

Demo only. See [docs/auth.md](docs/auth.md).

## Demo walkthrough

1. Start the app (`python app.py`).
2. Sign in with `admin` / `admin123`.
3. Add server `localhost` (name e.g. `demo-local`).
4. Watch dashboard panels (CPU, memory, disk, load, network, ports, processes) auto-refresh every 8s.
5. Log out — `/` redirects to login.

## Testing

```bash
pytest
ruff check app tests
```

CI runs the same on push/PR — see [docs/ci.md](docs/ci.md).

## Docs

- [docs/requirements.md](docs/requirements.md) — PRD  
- [docs/TODO.md](docs/TODO.md) — implementation checklist  
- [docs/inventory.md](docs/inventory.md) · [docs/metrics.md](docs/metrics.md) · [docs/ui.md](docs/ui.md)  
- [docs/acceptance.md](docs/acceptance.md) — verified acceptance criteria  
