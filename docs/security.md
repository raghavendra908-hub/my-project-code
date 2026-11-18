# Security notes (local demo)

| Control | Behavior |
|---------|----------|
| Bind address | `127.0.0.1` only |
| Auth | Single `admin` user; password stored as Werkzeug hash |
| CSRF | Flask-WTF on POST forms |
| Session cookie | `HttpOnly`, `SameSite=Lax` |
| Metrics | Read-only `psutil`; no process kill / shell |
| Inventory | In-memory; host field never used for remote I/O |
| Secrets | Do not commit `.env`; override `SECRET_KEY` via env if needed |

**Demo credentials** (`admin` / `admin123`) are for local demos only. Do not expose this app on a public interface.
