# Acceptance (PRD §7)

Verified locally: **2026-11-17**

- [x] Unauthenticated users cannot see metrics.
- [x] Login works with `admin` / `admin123`; password stored hashed.
- [x] User can add/list/remove server entries in memory.
- [x] Dashboard shows CPU, memory, disk, load average, network RX/TX, listening ports, and a bounded process list from the local machine.
- [x] Dashboard auto-refreshes.
- [x] UI is read-only and visually polished for a demo.
- [x] App runs locally with a short install/start path.

Out of scope confirmed unimplemented: remote SSH/agents, Windows hosts, alerts/history, multi-role auth, host mutations.
