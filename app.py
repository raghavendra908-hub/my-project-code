"""Run the local monitoring demo on 127.0.0.1 only."""

from __future__ import annotations

import os

from app import create_app

app = create_app()


if __name__ == "__main__":
    # Bind to loopback only — do not expose this demo on a public interface.
    # Keep debug off for shared/demo notes; enable locally via FLASK_DEBUG=1 if needed.
    # PORT env overrides 5000 when that port is already taken on a shared host.
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
