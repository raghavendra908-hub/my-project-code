"""WTForms used by the monitoring demo."""

from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(max=64)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(max=128)],
    )


class ServerForm(FlaskForm):
    name = StringField(
        "Name / label",
        validators=[DataRequired(), Length(max=64)],
    )
    host = StringField(
        "Hostname or IP",
        validators=[DataRequired(), Length(max=253)],
        default="localhost",
    )
    notes = TextAreaField(
        "Notes / tags",
        validators=[Optional(), Length(max=200)],
    )


class RemoveServerForm(FlaskForm):
    server_id = HiddenField(validators=[DataRequired()])
