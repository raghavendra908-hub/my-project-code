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
from app.forms import LoginForm, RemoveServerForm, ServerForm
from app.inventory import add_server, list_servers, remove_server
from app.metrics import REFRESH_SECONDS, collect_all

bp = Blueprint("main", __name__)


@bp.get("/")
@login_required
def dashboard():
    """Monitoring dashboard — requires an authenticated session."""
    metrics = collect_all()
    return render_template(
        "dashboard.html",
        username=current_user(),
        servers=list_servers(),
        metrics=metrics,
        refresh_seconds=REFRESH_SECONDS,
    )


@bp.get("/servers")
@login_required
def servers_page():
    """Inventory management page (add / remove servers)."""
    return render_template(
        "servers.html",
        username=current_user(),
        servers=list_servers(),
        server_form=ServerForm(),
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


@bp.post("/servers")
@login_required
def servers_add():
    """Add a server inventory entry (in-memory; metrics stay localhost)."""
    form = ServerForm()
    if form.validate_on_submit():
        try:
            add_server(
                name=form.name.data or "",
                host=form.host.data or "",
                notes=form.notes.data or "",
            )
            flash("Server added to inventory.", "ok")
        except ValueError as exc:
            flash(str(exc), "error")
    else:
        flash("Could not add server — check required fields.", "error")
    return redirect(url_for("main.servers_page"))


@bp.post("/servers/remove")
@login_required
def servers_remove():
    """Remove a server inventory entry by id."""
    form = RemoveServerForm()
    if form.validate_on_submit():
        raw = form.server_id.data or ""
        try:
            server_id = int(raw)
        except (TypeError, ValueError):
            flash("Invalid server id.", "error")
            return redirect(url_for("main.servers_page"))
        if remove_server(server_id):
            flash("Server removed from inventory.", "ok")
        else:
            flash("Server not found.", "error")
    else:
        flash("Could not remove server.", "error")
    return redirect(url_for("main.servers_page"))
