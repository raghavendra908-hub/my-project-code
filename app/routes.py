"""HTTP routes for the monitoring demo."""

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, url_for

from app.auth import (
    current_user,
    login_required,
    login_user,
    logout_user,
    verify_credentials,
)
from app.forms import LoginForm

bp = Blueprint("main", __name__)

# Placeholder panels — metrics wired in a later phase.
DASHBOARD_PANELS = (
    {"id": "cpu", "title": "CPU", "hint": "Overall usage %"},
    {"id": "memory", "title": "Memory", "hint": "Used / free"},
    {"id": "disk", "title": "Disk", "hint": "Root filesystem"},
    {"id": "load", "title": "Load average", "hint": "1 / 5 / 15 min"},
    {"id": "network", "title": "Network", "hint": "RX / TX"},
    {"id": "ports", "title": "Listening ports", "hint": "TCP / UDP"},
    {"id": "processes", "title": "Processes", "hint": "Top by CPU / memory"},
)


@bp.get("/")
@login_required
def dashboard():
    """Monitoring dashboard — requires an authenticated session."""
    return render_template(
        "dashboard.html",
        panels=DASHBOARD_PANELS,
        username=current_user(),
    )


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Sign in with the built-in admin account."""
    if current_user():
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        username = (form.username.data or "").strip()
        password = form.password.data or ""
        if verify_credentials(username, password):
            login_user(username)
            flash("Signed in successfully.", "ok")
            return redirect(url_for("main.dashboard"))
        flash("Invalid username or password.", "error")

    return render_template("login.html", form=form)


@bp.post("/logout")
@login_required
def logout():
    """Clear the session and return to the login page."""
    logout_user()
    flash("Signed out.", "ok")
    return redirect(url_for("main.login"))
