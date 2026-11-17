"""Flask application factory for the local monitoring demo."""

from __future__ import annotations

import os

from flask import Flask, flash, redirect, url_for
from flask_wtf.csrf import CSRFError, CSRFProtect

csrf = CSRFProtect()

# Stable local-demo default so CSRF/session survive process restarts during demos.
# Override with SECRET_KEY in the environment for anything beyond local use.
_DEMO_SECRET_KEY = "host-monitor-local-demo-only-not-for-production"


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the Flask app (localhost demo only)."""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(package_dir)

    app = Flask(
        __name__,
        template_folder=os.path.join(root_dir, "templates"),
        static_folder=os.path.join(root_dir, "static"),
    )

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or _DEMO_SECRET_KEY

    # Session cookie hardening for the local demo.
    # SESSION_COOKIE_SECURE should be True when serving over HTTPS.
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        WTF_CSRF_ENABLED=True,
    )

    if test_config:
        app.config.update(test_config)

    csrf.init_app(app)

    from app.routes import bp

    app.register_blueprint(bp)

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error: CSRFError):
        flash("Your sign-in form expired. Please try again.", "error")
        return redirect(url_for("main.login"))

    return app
