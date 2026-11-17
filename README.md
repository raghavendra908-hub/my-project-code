# Host Monitor (Local Demo)

Read-only web UI for live Linux host metrics (CPU, memory, disk, load, network, ports, processes) on the **same machine** where the app runs. Built for an internal L1/L2/L3 demo — not for public or multi-host production use.

**Security:** The app binds to `127.0.0.1` only. Do not expose it on a public interface. Do not commit secrets or a real `.env`. Passwords are stored hashed; monitoring pages require login.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For tests:

```bash
pip install -r requirements-dev.txt
```

## Run

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). You will be redirected to `/login`.

If port 5000 is already in use on a shared host:

```bash
PORT=5010 python app.py
```

Then open [http://127.0.0.1:5010](http://127.0.0.1:5010).

Optional: set `SECRET_KEY` in the environment before starting; otherwise a stable local-demo default is used (override for anything beyond local use).

## Sign in (demo)

| Username | Password |
|----------|----------|
| `admin` | `admin123` |

Demo credentials only — documented here for local use. See [docs/auth.md](docs/auth.md).

## Testing

```bash
pytest
```

## Dashboard panels

Placeholder panels (metrics not wired yet):

- CPU
- Memory
- Disk
- Load average
- Network
- Listening ports
- Processes

See [docs/requirements.md](docs/requirements.md), [docs/TODO.md](docs/TODO.md), [docs/ui.md](docs/ui.md), and [docs/auth.md](docs/auth.md).
