# Auth (Phase 1)

## Demo credentials

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

Demo only — change before any shared use. The app stores a **hash** of the password in `app/auth.py` (Werkzeug `scrypt`); plaintext is not kept in that module.

## Routes

| Method | Path | Behavior |
|--------|------|----------|
| GET/POST | `/login` | Sign-in form. Invalid credentials flash `Invalid username or password.` Successful login redirects to `/`. |
| POST | `/logout` | Clears session; redirects to `/login`. |
| GET | `/` | Dashboard — **login required**. Anonymous users redirect to `/login`. |

## Security notes

- Password checked with `werkzeug.security.check_password_hash` (constant-time compare vs stored hash).
- Login is POST-only for credentials; CSRF via Flask-WTF (`LoginForm` + `CSRFProtect`).
- Expired/missing CSRF tokens redirect back to `/login` with a clear flash (not a raw 400 page).
- Session cookie: `HttpOnly`, `SameSite=Lax`. Set `SESSION_COOKIE_SECURE=True` if you ever serve over HTTPS.
- `SECRET_KEY` defaults to a stable local-demo value so form sessions survive restarts; override via env for anything else.
- Unauthenticated users cannot see metrics pages.
