# Server inventory (Phase 2)

In-memory demo inventory. **Restart clears the list.** There is no database.

## Fields

| Field | Required | Max length | Notes |
|-------|----------|------------|-------|
| Name / label | yes | 64 | Display name |
| Hostname or IP | yes | 253 | For demo UI only — use `localhost` / `127.0.0.1` |
| Notes / tags | no | 200 | Free text |

Inputs are trimmed; control characters are stripped. Hostnames are **never** passed to a shell or used for remote collection.

## Flows

| Action | Method | Path | Auth |
|--------|--------|------|------|
| Add | POST | `/servers` | required + CSRF |
| Remove | POST | `/servers/remove` | required + CSRF (`server_id`) |
| List | GET | `/` (dashboard strip) | required |

## Localhost-only metrics rule

Live metrics always come from the machine running Flask, even if inventory lists another host. The dashboard banner states this clearly. No SSH keys, agents, or remote sockets.
